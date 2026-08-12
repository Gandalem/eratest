#!/usr/bin/env python3
"""Classify legacy Korean ERB text for safe migration onto ``main``.

The legacy Korean branch has a different Git ancestry from ``main``.  This
tool deliberately does not merge files.  It masks only player-visible text,
keeps executable expressions in the code skeleton, and reports which files or
functions can be used as string-migration sources.

Typical use for PR #1::

    python .github/scripts/korean_string_migration.py analyze \
      --repo . --main-ref origin/main \
      --legacy-base-ref origin/korean \
      --legacy-ref origin/codex/korean-pass-65 \
      --output-dir migration-report-pr1

Future translation commits can be guarded with ``verify``.  Verification
fails when executable ERB structure differs from the selected main baseline.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
SCANNER_PATH = SCRIPT_DIR / "translation_progress_v2.py"
ERB_SUFFIXES = {".erb", ".erh"}
FUNCTION_RE = re.compile(r"^\s*@([^\s(]+)")
HANGUL_RE = re.compile(r"[가-힣]")


def load_scanner():
    spec = importlib.util.spec_from_file_location(
        "translation_progress_v2_for_migration", SCANNER_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load scanner: {SCANNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SCANNER = load_scanner()


@dataclass(frozen=True)
class Section:
    name: str
    start_line: int
    end_line: int
    skeleton: tuple[str, ...]
    visible: tuple[str, ...]
    korean_visible: int
    mask_misses: int


@dataclass(frozen=True)
class FileResult:
    path: str
    classification: str
    reason: str
    legacy_visible: int
    legacy_korean_visible: int
    candidate_sections: int
    matched_sections: int
    unmatched_sections: tuple[str, ...]
    main_skeleton_sha256: str
    legacy_skeleton_sha256: str
    mask_misses: int
    safe_scope: str = "none"
    matched_section_names: tuple[str, ...] = ()


class GitError(RuntimeError):
    pass


def run_git(repo: Path, args: Sequence[str], *, check: bool = True) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and completed.returncode:
        message = completed.stderr.decode("utf-8", errors="replace").strip()
        raise GitError(f"git {' '.join(args)} failed: {message}")
    return completed.stdout


def ref_exists(repo: Path, ref: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", ref],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def blob_exists(repo: Path, ref: str, path: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{ref}:{path}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def read_blob(repo: Path, ref: str, path: str) -> str:
    raw = run_git(repo, ["show", f"{ref}:{path}"])
    for encoding in ("utf-8-sig", "cp932"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace")


def changed_erb_paths(repo: Path, base_ref: str, head_ref: str) -> list[str]:
    raw = run_git(
        repo,
        ["diff", "--name-only", "-z", base_ref, head_ref, "--", "ERB"],
    )
    paths = [item.decode("utf-8", errors="surrogateescape") for item in raw.split(b"\0") if item]
    return sorted(
        path for path in paths if Path(path).suffix.casefold() in ERB_SUFFIXES
    )


def strip_comment(line: str) -> str:
    """Remove an ERB comment while respecting quotes and escaped quotes."""

    in_quote = False
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_quote:
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
            continue
        if char == ";" and not in_quote:
            return line[:index]
    return line


def mask_visible_payload(text: str) -> str:
    """Mask prose but retain ERB expressions embedded in visible text.

    Percent expressions and brace expressions are executable and therefore
    remain byte-for-byte significant.  Inline ``\\@ ... \\@`` conditionals are
    kept whole; this is intentionally conservative because they mix code and
    display branches and should be reviewed unless unchanged.
    """

    output: list[str] = []
    prose_pending = False
    index = 0

    def flush_prose() -> None:
        nonlocal prose_pending
        if prose_pending:
            output.append("<TEXT>")
            prose_pending = False

    while index < len(text):
        if text.startswith(r"\@", index):
            end = text.find(r"\@", index + 2)
            if end >= 0:
                flush_prose()
                output.append(text[index : end + 2])
                index = end + 2
                continue
        char = text[index]
        if char == "%":
            end = text.find("%", index + 1)
            if end >= 0:
                flush_prose()
                output.append(text[index : end + 1])
                index = end + 1
                continue
        if char == "{":
            end = text.find("}", index + 1)
            if end >= 0:
                flush_prose()
                output.append(text[index : end + 1])
                index = end + 1
                continue
        if not char.isspace():
            prose_pending = True
        index += 1
    flush_prose()
    return "".join(output) or "<TEXT>"


def visible_segments(
    line: str,
    *,
    path: str = "",
    line_number: int = 0,
    section_name: str = "",
) -> tuple[str, ...]:
    if section_name.upper() in SCANNER.INTERNAL_ONLY_FUNCTIONS:
        return ()
    if path and SCANNER.is_excluded_reference_path(path):
        return ()
    if path and SCANNER.is_excluded_reference_line(path, line_number):
        return ()
    if path and SCANNER.is_path_internal_line(path, line):
        return ()
    try:
        return tuple(SCANNER.extract_strings(line))
    except Exception:
        # Analysis must fail closed.  Leaving a line unmasked makes it require
        # review instead of accidentally calling it safe.
        return ()


def skeletonize_line(
    line: str,
    *,
    path: str = "",
    line_number: int = 0,
    section_name: str = "",
) -> tuple[str, tuple[str, ...], int]:
    code = strip_comment(line).strip()
    if not code:
        return "", (), 0
    segments = visible_segments(
        code,
        path=path,
        line_number=line_number,
        section_name=section_name,
    )
    masked = code
    misses = 0
    search_from = 0
    for segment in segments:
        position = masked.find(segment, search_from)
        if position < 0:
            # Nested ERB strings occasionally defeat the lightweight scanner.
            # Keep the original line so it cannot be automatically accepted.
            misses += 1
            continue
        replacement = mask_visible_payload(segment)
        masked = masked[:position] + replacement + masked[position + len(segment) :]
        search_from = position + len(replacement)
    masked = re.sub(r"\s+", " ", masked).strip()
    return masked, segments, misses


def make_section(name: str, start: int, lines: Sequence[str], path: str = "") -> Section:
    skeleton: list[str] = []
    visible: list[str] = []
    misses = 0
    for offset, line in enumerate(lines):
        masked, segments, line_misses = skeletonize_line(
            line,
            path=path,
            line_number=start + offset,
            section_name=name,
        )
        if masked:
            skeleton.append(masked)
        visible.extend(segments)
        misses += line_misses
    korean = sum(bool(HANGUL_RE.search(item)) for item in visible)
    return Section(
        name=name,
        start_line=start,
        end_line=start + max(0, len(lines) - 1),
        skeleton=tuple(skeleton),
        visible=tuple(visible),
        korean_visible=korean,
        mask_misses=misses,
    )


def split_sections(text: str, path: str = "") -> list[Section]:
    lines = text.splitlines()
    sections: list[Section] = []
    current_name = "__preamble__"
    current_start = 1
    current_lines: list[str] = []
    for line_number, line in enumerate(lines, 1):
        match = FUNCTION_RE.match(line)
        if match:
            if current_lines:
                sections.append(make_section(current_name, current_start, current_lines, path))
            current_name = match.group(1).casefold()
            current_start = line_number
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines:
        sections.append(make_section(current_name, current_start, current_lines, path))
    return sections


def file_skeleton(sections: Iterable[Section]) -> tuple[str, ...]:
    result: list[str] = []
    for section in sections:
        result.extend(section.skeleton)
    return tuple(result)


def skeleton_hash(skeleton: Sequence[str]) -> str:
    if not skeleton:
        return ""
    return hashlib.sha256("\n".join(skeleton).encode("utf-8")).hexdigest()


def section_index(sections: Iterable[Section]) -> dict[str, list[Section]]:
    result: dict[str, list[Section]] = defaultdict(list)
    for section in sections:
        result[section.name].append(section)
    return result


def analyze_file(repo: Path, main_ref: str, legacy_ref: str, path: str) -> FileResult:
    if not blob_exists(repo, legacy_ref, path):
        return FileResult(path, "code_only", "legacy head no longer contains file", 0, 0, 0, 0, (), "", "", 0)
    legacy_sections = split_sections(read_blob(repo, legacy_ref, path), path)
    legacy_skeleton = file_skeleton(legacy_sections)
    legacy_visible = sum(len(section.visible) for section in legacy_sections)
    legacy_korean = sum(section.korean_visible for section in legacy_sections)
    legacy_misses = sum(section.mask_misses for section in legacy_sections)

    if not blob_exists(repo, main_ref, path):
        return FileResult(
            path,
            "deleted",
            "path does not exist on main; do not resurrect it",
            legacy_visible,
            legacy_korean,
            0,
            0,
            (),
            "",
            skeleton_hash(legacy_skeleton),
            legacy_misses,
        )

    main_sections = split_sections(read_blob(repo, main_ref, path), path)
    main_skeleton = file_skeleton(main_sections)
    main_index = section_index(main_sections)
    legacy_index = section_index(legacy_sections)

    candidate_sections: list[Section] = []
    for legacy in legacy_sections:
        peers = main_index.get(legacy.name, [])
        main_visible = peers[0].visible if len(peers) == 1 else ()
        if legacy.korean_visible and legacy.visible != main_visible:
            candidate_sections.append(legacy)

    common_misses = legacy_misses + sum(section.mask_misses for section in main_sections)
    if not candidate_sections:
        return FileResult(
            path,
            "code_only",
            "no differing Korean player-visible text detected",
            legacy_visible,
            legacy_korean,
            0,
            0,
            (),
            skeleton_hash(main_skeleton),
            skeleton_hash(legacy_skeleton),
            common_misses,
        )

    if common_misses == 0 and main_skeleton == legacy_skeleton:
        return FileResult(
            path,
            "automatic",
            "entire executable skeleton matches",
            legacy_visible,
            legacy_korean,
            len(candidate_sections),
            len(candidate_sections),
            (),
            skeleton_hash(main_skeleton),
            skeleton_hash(legacy_skeleton),
            0,
            safe_scope="file",
            matched_section_names=tuple(sorted(section.name for section in candidate_sections)),
        )

    matched = 0
    matched_names: list[str] = []
    unmatched: list[str] = []
    for legacy in candidate_sections:
        legacy_peers = legacy_index.get(legacy.name, [])
        main_peers = main_index.get(legacy.name, [])
        if (
            common_misses == 0
            and len(legacy_peers) == 1
            and len(main_peers) == 1
            and legacy.skeleton == main_peers[0].skeleton
        ):
            matched += 1
            matched_names.append(legacy.name)
        else:
            unmatched.append(legacy.name)

    if matched == len(candidate_sections):
        classification = "automatic"
        reason = "all translated functions have matching executable skeletons"
    elif matched:
        classification = "partial"
        reason = "only some translated functions have matching executable skeletons"
    else:
        classification = "structure_changed"
        reason = "no translated function has an unchanged executable skeleton"
    if common_misses:
        classification = "structure_changed" if not matched else "partial"
        reason += f"; {common_misses} visible-string mask miss(es) require review"

    return FileResult(
        path,
        classification,
        reason,
        legacy_visible,
        legacy_korean,
        len(candidate_sections),
        matched,
        tuple(sorted(set(unmatched))),
        skeleton_hash(main_skeleton),
        skeleton_hash(legacy_skeleton),
        common_misses,
        safe_scope="functions" if matched else "none",
        matched_section_names=tuple(sorted(set(matched_names))),
    )


def write_report(
    output_dir: Path,
    results: Sequence[FileResult],
    *,
    main_ref: str,
    legacy_base_ref: str,
    legacy_ref: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = Counter(item.classification for item in results)
    automatic_scopes = Counter(
        item.safe_scope for item in results if item.classification == "automatic"
    )
    payload = {
        "version": 1,
        "main_ref": main_ref,
        "legacy_base_ref": legacy_base_ref,
        "legacy_ref": legacy_ref,
        "candidate_files": len(results),
        "counts": dict(sorted(counts.items())),
        "automatic_scopes": dict(sorted(automatic_scopes.items())),
        "files": [asdict(item) for item in results],
    }
    (output_dir / "report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with (output_dir / "files.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "classification", "safe_scope", "path", "reason", "legacy_visible",
                "legacy_korean_visible", "candidate_sections", "matched_sections",
                "matched_section_names", "unmatched_sections", "mask_misses",
                "main_skeleton_sha256",
                "legacy_skeleton_sha256",
            ]
        )
        for item in results:
            writer.writerow(
                [
                    item.classification, item.safe_scope, item.path, item.reason,
                    item.legacy_visible, item.legacy_korean_visible,
                    item.candidate_sections, item.matched_sections,
                    " | ".join(item.matched_section_names),
                    " | ".join(item.unmatched_sections),
                    item.mask_misses, item.main_skeleton_sha256,
                    item.legacy_skeleton_sha256,
                ]
            )

    for classification in (
        "automatic", "partial", "structure_changed", "deleted", "code_only"
    ):
        lines = [item.path for item in results if item.classification == classification]
        (output_dir / f"{classification}.txt").write_text(
            "".join(f"{line}\n" for line in lines), encoding="utf-8"
        )

    automatic_files = [
        item.path for item in results
        if item.classification == "automatic" and item.safe_scope == "file"
    ]
    (output_dir / "automatic-files.txt").write_text(
        "".join(f"{path}\n" for path in automatic_files), encoding="utf-8"
    )
    for filename, classification in (
        ("automatic-functions.tsv", "automatic"),
        ("partial-functions.tsv", "partial"),
    ):
        rows = ["file\tmatched_functions\n"]
        for item in results:
            if item.classification == classification and item.safe_scope == "functions":
                rows.append(
                    f"{item.path}\t{' | '.join(item.matched_section_names)}\n"
                )
        (output_dir / filename).write_text("".join(rows), encoding="utf-8")

    summary = [
        "# korean-next 번역 문자열 마이그레이션 분석",
        "",
        f"- 최신 코드 기준: `{main_ref}`",
        f"- legacy 변경 기준: `{legacy_base_ref}` → `{legacy_ref}`",
        f"- 분석 파일: **{len(results)}개**",
        "",
        "| 분류 | 파일 수 | 처리 원칙 |",
        "|---|---:|---|",
        f"| 자동 이식 가능 | {counts['automatic']} | 동일 코드 골격의 표시 문자열만 배치 이식 |",
        f"| └ 파일 골격 전체 동일 | {automatic_scopes['file']} | 파일의 표시 문자열 매핑 가능 |",
        f"| └ 안전 함수만 동일 | {automatic_scopes['functions']} | 명시된 함수의 표시 문자열만 매핑 |",
        f"| 부분 이식 가능 | {counts['partial']} | 일치 함수만 이식하고 나머지는 검토 |",
        f"| 구조 변경 | {counts['structure_changed']} | 수동 문맥 검토 전 이식 금지 |",
        f"| main에서 삭제됨 | {counts['deleted']} | 번역 폐기, 파일 복원 금지 |",
        f"| 코드 전용/이미 반영 | {counts['code_only']} | 이식 대상에서 제외 |",
        "",
        "## 안전 원칙",
        "",
        "- 이 보고서는 파일을 수정하지 않는다.",
        "- `%...%`, `{...}`, `\\@...\\@` 표현은 코드 골격에 남긴다.",
        "- main에 없는 파일은 자동으로 `deleted` 처리한다.",
        "- 마스킹에 실패한 줄은 자동 이식으로 분류하지 않는다.",
        "- 실제 이식 후에는 `verify` 모드로 main 대비 코드 골격 불변을 검사한다.",
        "",
    ]
    (output_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")


def command_analyze(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    for ref in (args.main_ref, args.legacy_base_ref, args.legacy_ref):
        if not ref_exists(repo, ref):
            raise SystemExit(f"unknown git ref: {ref}")
    paths = changed_erb_paths(repo, args.legacy_base_ref, args.legacy_ref)
    results = [analyze_file(repo, args.main_ref, args.legacy_ref, path) for path in paths]
    write_report(
        Path(args.output_dir).resolve(),
        results,
        main_ref=args.main_ref,
        legacy_base_ref=args.legacy_base_ref,
        legacy_ref=args.legacy_ref,
    )
    counts = Counter(item.classification for item in results)
    print(f"candidate_files={len(results)}")
    for name in ("automatic", "partial", "structure_changed", "deleted", "code_only"):
        print(f"{name}={counts[name]}")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    for ref in (args.base_ref, args.candidate_ref):
        if not ref_exists(repo, ref):
            raise SystemExit(f"unknown git ref: {ref}")
    paths = changed_erb_paths(repo, args.base_ref, args.candidate_ref)
    failures: list[str] = []
    for path in paths:
        if not blob_exists(repo, args.base_ref, path) or not blob_exists(repo, args.candidate_ref, path):
            failures.append(f"{path}: file added/deleted")
            continue
        base_sections = split_sections(read_blob(repo, args.base_ref, path), path)
        candidate_sections = split_sections(read_blob(repo, args.candidate_ref, path), path)
        misses = sum(section.mask_misses for section in base_sections + candidate_sections)
        if misses:
            failures.append(f"{path}: {misses} visible-string mask miss(es)")
            continue
        if file_skeleton(base_sections) != file_skeleton(candidate_sections):
            failures.append(f"{path}: executable skeleton changed")
    if failures:
        print("code-protection: FAILED", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"code-protection: ok ({len(paths)} changed ERB files)")
    return 0


def self_test() -> int:
    assert strip_comment('PRINTL "semi;colon" ; comment') == 'PRINTL "semi;colon" '
    assert mask_visible_payload("안녕 %CALLNAME:TARGET%!") == "<TEXT>%CALLNAME:TARGET%<TEXT>"
    assert mask_visible_payload("Hello {LOCAL}") == "<TEXT>{LOCAL}"
    assert mask_visible_payload(r"앞 \@ FLAG ? 참 # 거짓 \@ 뒤") == r"<TEXT>\@ FLAG ? 참 # 거짓 \@<TEXT>"

    main = """@MENU\n#DIM LOCAL\nIF FLAG:1\nPRINTFORMW Hello %CALLNAME:TARGET%\nENDIF\n"""
    korean = """@MENU\n#DIM LOCAL\nIF FLAG:1\nPRINTFORMW 안녕 %CALLNAME:TARGET%\nENDIF\n"""
    changed_code = """@MENU\n#DIM LOCAL\nIF FLAG:2\nPRINTFORMW 안녕 %CALLNAME:TARGET%\nENDIF\n"""
    main_sections = split_sections(main)
    korean_sections = split_sections(korean)
    changed_sections = split_sections(changed_code)
    assert file_skeleton(main_sections) == file_skeleton(korean_sections)
    assert file_skeleton(main_sections) != file_skeleton(changed_sections)
    assert korean_sections[0].korean_visible == 1

    internal_main = 'CALL GET_STR(MASTER, "Weapon", ARG, "Class")\n'
    internal_changed = 'CALL GET_STR(MASTER, "무기", ARG, "Class")\n'
    assert file_skeleton(split_sections(internal_main)) != file_skeleton(split_sections(internal_changed))
    internal_function_main = '@PEE_PAD_NEEDED(ARG)\nRETURNF "Bulky Liner"\n'
    internal_function_changed = '@PEE_PAD_NEEDED(ARG)\nRETURNF "두꺼운 라이너"\n'
    assert file_skeleton(split_sections(internal_function_main)) != file_skeleton(
        split_sections(internal_function_changed)
    )
    path_key_main = 'SFSR_TYPE \'= "Love Route"\n'
    path_key_changed = 'SFSR_TYPE \'= "연애 경로"\n'
    better_ui_path = "ERB/TRANSLATION/ANON/BetterUI.ERB"
    assert file_skeleton(split_sections(path_key_main, better_ui_path)) != file_skeleton(
        split_sections(path_key_changed, better_ui_path)
    )
    print("self-test: ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="classify legacy translation files")
    analyze.add_argument("--repo", default=".")
    analyze.add_argument("--main-ref", required=True)
    analyze.add_argument("--legacy-base-ref", required=True)
    analyze.add_argument("--legacy-ref", required=True)
    analyze.add_argument("--output-dir", required=True)
    analyze.set_defaults(func=command_analyze)

    verify = subparsers.add_parser("verify", help="fail if ERB executable skeleton changed")
    verify.add_argument("--repo", default=".")
    verify.add_argument("--base-ref", required=True)
    verify.add_argument("--candidate-ref", required=True)
    verify.set_defaults(func=command_verify)

    test = subparsers.add_parser("self-test", help="run parser and skeleton regression tests")
    test.set_defaults(func=lambda _args: self_test())
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
