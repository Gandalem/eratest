#!/usr/bin/env python3
"""Heuristic Korean translation progress scanner for ERB/ERH sources.

Compares the original/main tree with the korean tree using the same extraction
rules. The primary metric is the reduction of meaningful English prose
characters, reported overall and by content category. It also reports remaining
English-only, mixed Korean/English, Korean-containing, and Japanese-kana units.

This is intentionally a localization scanner, not an ERB parser. Its output is
best used as a trend/progress metric and a work queue, not as a proof that every
string is translated correctly.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

ROOTS = (Path("ERB/TRANSLATION"), Path("ERB/NEWGAME"), Path("ERB/MOVEMENTS"))
EXTS = {".ERB", ".ERH"}

# These tokens are used only to decide whether a line can plausibly emit or
# return user-visible text. PRINT* lines receive special handling below.
VISIBLE_TOKENS = (
    "RETURNF",
    "LOCALS",
    "RESULTS",
    "MAKE_STR",
    "ASK_",
    "HTML",
    "BUTTON",
    "CHOICES",
    "TITLE",
    "DESC",
    "MESSAGE",
    "NAME",
    "SFSR_",
)

QUOTED_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')
PRINT_RE = re.compile(r"^\s*(PRINT[A-Z0-9_]*)\b(.*)$", re.IGNORECASE)
EN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]{2,}")
HANGUL_RE = re.compile(r"[가-힣]")
KANA_RE = re.compile(r"[ぁ-ゟ゠-ヿ]")
FORMAT_PERCENT_RE = re.compile(r"%[^%\r\n]+%")
FORMAT_BRACE_RE = re.compile(r"\{[^{}\r\n]+\}")
HTML_TAG_RE = re.compile(r"<[^>]+>")
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
ESCAPE_RE = re.compile(r"\\(?:n|r|t|%|N)")

# Common abbreviations / domain words that should not make an otherwise Korean
# string look untranslated. Proper nouns are deliberately kept conservative:
# unknown names remain visible in the mixed-string review queue.
ENGLISH_ALLOWLIST = {
    "hp", "mp", "sp", "sta", "ene", "exp", "cm", "tsp", "ui", "ux", "ai",
    "html", "nas", "erb", "erh", "fps", "rpm", "usb", "vr", "rpg", "npc",
    "pc", "cpu", "gpu", "ram", "hdd", "ssd", "ddr", "posix", "api",
    "touhou", "gensokyo", "youkai", "danmaku", "youjutsu", "makai",
}

# Known schema/data keys that can appear inside a visible expression but are not
# themselves UI text. Keep this list narrow; false negatives are preferable to
# silently hiding real labels.
INTERNAL_LITERAL_ALLOWLIST = {
    "hediff type", "disease", "drug", "shortname", "weaponammo",
}

# Very short labels that the normal 3+ letter word detector would miss. They
# are counted only when they effectively make up the whole visible unit.
SHORT_ENGLISH_LABELS = {"m", "h", "s", "n/a", "na", "yes", "no", "on", "off", "ok"}

CATEGORY_ORDER = (
    "ui_menu",
    "help_tooltip",
    "item_description",
    "dialogue_event",
    "lore_internet",
    "debug_tools",
    "other_visible",
)
CATEGORY_LABELS = {
    "ui_menu": "UI/메뉴",
    "help_tooltip": "도움말/툴팁",
    "item_description": "아이템 설명",
    "dialogue_event": "대사/이벤트",
    "lore_internet": "세계관/인터넷/뉴스",
    "debug_tools": "디버그/도구",
    "other_visible": "기타 화면 문자열",
}


@dataclass(frozen=True)
class Unit:
    path: str
    line: int
    category: str
    raw: str
    normalized: str
    english_words: tuple[str, ...]
    english_chars: int
    hangul_chars: int
    kana_chars: int
    state: str


@dataclass
class Metrics:
    units: int = 0
    english_chars: int = 0
    english_only: int = 0
    mixed: int = 0
    korean_only: int = 0
    japanese: int = 0
    foreign_other: int = 0

    def add(self, unit: Unit) -> None:
        self.units += 1
        self.english_chars += unit.english_chars
        if unit.kana_chars > 0:
            self.japanese += 1
        if unit.state == "english_only":
            self.english_only += 1
        elif unit.state == "mixed":
            self.mixed += 1
        elif unit.state == "korean_only":
            self.korean_only += 1
        elif unit.state not in {"japanese"}:
            self.foreign_other += 1


def meaningful_english_words(text: str) -> list[str]:
    words = []
    for match in EN_WORD_RE.finditer(text):
        word = match.group(0)
        folded = word.casefold()
        if folded in ENGLISH_ALLOWLIST:
            continue
        # Short all-caps tokens are overwhelmingly stats, caliber names, or UI
        # abbreviations rather than prose.
        letters = re.sub(r"[^A-Za-z]", "", word)
        if letters.isupper() and len(letters) <= 6:
            continue
        words.append(word)

    if not words:
        compact = re.sub(r"[^a-z/]+", "", text.casefold())
        if compact in SHORT_ENGLISH_LABELS:
            words.append(compact)
    return words


def normalize_for_language(text: str) -> str:
    text = URL_RE.sub(" ", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = FORMAT_PERCENT_RE.sub(" ", text)
    text = FORMAT_BRACE_RE.sub(" ", text)
    text = ESCAPE_RE.sub(" ", text)
    # Keep the text inside ERB inline conditional expressions; only remove the
    # delimiter itself so both visible branches remain measurable.
    text = text.replace(r"\@", " ")
    text = text.replace("＠", " ")
    return " ".join(text.split())


def classify_state(normalized: str) -> tuple[str, tuple[str, ...], int, int, int]:
    words = tuple(meaningful_english_words(normalized))
    en_chars = sum(sum(ch.isalpha() and ch.isascii() for ch in word) for word in words)
    hangul_chars = len(HANGUL_RE.findall(normalized))
    kana_chars = len(KANA_RE.findall(normalized))

    has_en = en_chars > 0
    has_ko = hangul_chars > 0
    has_ja = kana_chars > 0

    if has_ko and has_en:
        state = "mixed"
    elif has_ko:
        state = "korean_only"
    elif has_en:
        state = "english_only"
    elif has_ja:
        state = "japanese"
    else:
        state = "foreign_other"
    return state, words, en_chars, hangul_chars, kana_chars


def is_internal_literal(text: str) -> bool:
    stripped = text.strip()
    folded = stripped.casefold()
    if folded in INTERNAL_LITERAL_ALLOWLIST:
        return True
    if not stripped:
        return True
    # Strong identifier signals only. Do not suppress ordinary labels like
    # "Body Parts" or "Skill Acquisition".
    if re.fullmatch(r"[A-Za-z0-9_./:+()\-]{1,64}", stripped):
        if "_" in stripped or stripped.isupper():
            return True
    return False


def extract_strings(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped or stripped.startswith((";", "#")):
        return []

    print_match = PRINT_RE.match(line)
    upper = line.upper()
    if not print_match and not any(token in upper for token in VISIBLE_TOKENS):
        return []

    quoted = [m.group(1) for m in QUOTED_RE.finditer(line)]
    visible_quoted = [q for q in quoted if not is_internal_literal(q)]
    if visible_quoted:
        return visible_quoted

    # v1 missed unquoted PRINT/PRINTFORM strings entirely. For a PRINT* line
    # with no quotes, scan the payload after the opcode. Format placeholders are
    # removed later by normalize_for_language().
    if print_match:
        payload = print_match.group(2).strip()
        if payload and not is_internal_literal(payload):
            return [payload]
    return []


def classify_category(path: str, text: str, line: str) -> str:
    p = path.replace("\\", "/").casefold()
    normalized = normalize_for_language(text)
    length = len(normalized)

    if "debug" in p or "/cheat/" in p:
        return "debug_tools"

    lore_markers = (
        "/internet/", "/lore/", "new_update", "updatenewsletter", "newspaper",
        "danmaku world", "/ezb/",
    )
    if any(marker in p for marker in lore_markers):
        return "lore_internet"

    help_markers = (
        "html_mouseover", "nas_tips", "talent_info", "tooltip", "/help/",
        "tutorial", "manual", "guide",
    )
    if any(marker in p for marker in help_markers) or re.search(r"\bDESC\b", line.upper()):
        return "help_tooltip"

    item_path = "/item/" in p or p.endswith("/_tr lib.erb") or p.endswith("/_tr%20lib.erb")
    if item_path and length >= 100:
        return "item_description"

    dialogue_markers = (
        "/chara/", "/com/", "/daily events/", "/movements/", "kojo", "conversation",
        "/addition/", "lucid_", "event",
    )
    if any(marker in p for marker in dialogue_markers):
        return "dialogue_event"

    ui_path_markers = (
        "betterui", "item modding", "menu", "setting", "option", "config", "status",
        "shop", "store", "calendar", "character_profile", "character_dialog_status",
    )
    ui_line_markers = ("BUTTON", "CHOICES", "TITLE", "ASK_", "HTML", "SFSR_", "LOCALS")
    if any(marker in p for marker in ui_path_markers):
        return "ui_menu"
    if any(marker in line.upper() for marker in ui_line_markers) and length <= 180:
        return "ui_menu"
    if item_path and length < 100:
        return "ui_menu"
    if PRINT_RE.match(line) and length <= 100:
        return "ui_menu"

    return "other_visible"


def iter_source_files(root: Path) -> Iterable[Path]:
    for rel_root in ROOTS:
        base = root / rel_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.upper() in EXTS:
                yield path


def scan_tree(root: Path) -> list[Unit]:
    units: list[Unit] = []
    for path in iter_source_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="ignore").splitlines()
        except OSError as exc:
            print(f"warning: failed to read {path}: {exc}", file=sys.stderr)
            continue
        for line_no, line in enumerate(lines, 1):
            for raw in extract_strings(line):
                normalized = normalize_for_language(raw)
                state, words, en_chars, ko_chars, kana_chars = classify_state(normalized)
                # If none of the language signals are present, it is not useful
                # for translation progress and is discarded.
                if not (en_chars or ko_chars or kana_chars):
                    continue
                category = classify_category(rel, raw, line)
                units.append(
                    Unit(
                        path=rel,
                        line=line_no,
                        category=category,
                        raw=raw,
                        normalized=normalized,
                        english_words=words,
                        english_chars=en_chars,
                        hangul_chars=ko_chars,
                        kana_chars=kana_chars,
                        state=state,
                    )
                )
    return units


def aggregate(units: Iterable[Unit]) -> dict[str, Metrics]:
    metrics = {category: Metrics() for category in CATEGORY_ORDER}
    for unit in units:
        metrics.setdefault(unit.category, Metrics()).add(unit)
    return metrics


def total_metrics(metrics: dict[str, Metrics], categories: Optional[set[str]] = None) -> Metrics:
    result = Metrics()
    for category, value in metrics.items():
        if categories is not None and category not in categories:
            continue
        result.units += value.units
        result.english_chars += value.english_chars
        result.english_only += value.english_only
        result.mixed += value.mixed
        result.korean_only += value.korean_only
        result.japanese += value.japanese
        result.foreign_other += value.foreign_other
    return result


def reduction_pct(source: int, target: int) -> Optional[float]:
    if source <= 0:
        return None
    return (source - target) * 100.0 / source


def fmt_pct(value: Optional[float]) -> str:
    return "N/A" if value is None else f"{value:.1f}%"


def rows_for_report(source: dict[str, Metrics], target: dict[str, Metrics]) -> list[dict[str, object]]:
    rows = []
    for category in CATEGORY_ORDER:
        s = source.get(category, Metrics())
        t = target.get(category, Metrics())
        rows.append(
            {
                "category": category,
                "label": CATEGORY_LABELS[category],
                "source_units": s.units,
                "target_units": t.units,
                "source_english_chars": s.english_chars,
                "target_english_chars": t.english_chars,
                "english_reduction_pct": reduction_pct(s.english_chars, t.english_chars),
                "target_english_only": t.english_only,
                "target_mixed": t.mixed,
                "target_korean_only": t.korean_only,
                "target_japanese": t.japanese,
            }
        )
    return rows


def top_remaining_files(units: Iterable[Unit], limit: int = 30) -> list[dict[str, object]]:
    english_chars = Counter()
    english_only = Counter()
    mixed = Counter()
    categories: dict[str, Counter] = defaultdict(Counter)
    for unit in units:
        if unit.english_chars <= 0:
            continue
        english_chars[unit.path] += unit.english_chars
        categories[unit.path][unit.category] += unit.english_chars
        if unit.state == "english_only":
            english_only[unit.path] += 1
        elif unit.state == "mixed":
            mixed[unit.path] += 1
    result = []
    for path, chars in english_chars.most_common(limit):
        category = categories[path].most_common(1)[0][0] if categories[path] else "other_visible"
        result.append(
            {
                "path": path,
                "category": category,
                "english_chars": chars,
                "english_only": english_only[path],
                "mixed": mixed[path],
            }
        )
    return result


def top_review_units(units: Iterable[Unit], state: str, limit: int = 50) -> list[dict[str, object]]:
    selected = [u for u in units if u.state == state]
    selected.sort(key=lambda u: (u.english_chars, len(u.normalized)), reverse=True)
    return [
        {
            "path": u.path,
            "line": u.line,
            "category": u.category,
            "english_chars": u.english_chars,
            "text": u.raw[:500],
        }
        for u in selected[:limit]
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else ["category"]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def make_markdown(
    source_ref: str,
    target_ref: str,
    source_metrics: dict[str, Metrics],
    target_metrics: dict[str, Metrics],
    rows: list[dict[str, object]],
    top_files: list[dict[str, object]],
) -> str:
    s_total = total_metrics(source_metrics)
    t_total = total_metrics(target_metrics)
    core_categories = {"ui_menu", "help_tooltip"}
    s_core = total_metrics(source_metrics, core_categories)
    t_core = total_metrics(target_metrics, core_categories)

    lines = [
        "# 한글패치 진행률 스캐너 v2",
        "",
        f"- 원본 기준: `{source_ref}`",
        f"- 한글화 대상: `{target_ref}`",
        f"- 생성 시각(UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "- 진행률 정의: 동일 스캔 규칙에서 **의미 있는 영문 단어 문자 수가 원본 대비 얼마나 감소했는지**",
        "- 주의: 휴리스틱 스캐너이므로 번역 품질/문맥 정확성 자체를 보증하지는 않음",
        "",
        "## 핵심 지표",
        "",
        "| 범위 | 영문 감소율 | 원본 영문 문자 | 남은 영문 문자 | 영어 전용 문자열 | 한/영 혼합 문자열 | 한글 문자열 |",
        "|---|---:|---:|---:|---:|---:|---:|",
        f"| 전체 | {fmt_pct(reduction_pct(s_total.english_chars, t_total.english_chars))} | {s_total.english_chars:,} | {t_total.english_chars:,} | {t_total.english_only:,} | {t_total.mixed:,} | {t_total.korean_only:,} |",
        f"| 핵심 UI+도움말 | {fmt_pct(reduction_pct(s_core.english_chars, t_core.english_chars))} | {s_core.english_chars:,} | {t_core.english_chars:,} | {t_core.english_only:,} | {t_core.mixed:,} | {t_core.korean_only:,} |",
        "",
        "## 영역별 진행률",
        "",
        "| 영역 | 영문 감소율 | 원본 영문 문자 | 남은 영문 문자 | 영어 전용 | 혼합 | 한글 | 일본어 후보 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['label']} | {fmt_pct(row['english_reduction_pct'])} | "
            f"{int(row['source_english_chars']):,} | {int(row['target_english_chars']):,} | "
            f"{int(row['target_english_only']):,} | {int(row['target_mixed']):,} | "
            f"{int(row['target_korean_only']):,} | {int(row['target_japanese']):,} |"
        )

    lines.extend([
        "",
        "## 남은 영어가 많은 파일",
        "",
        "| 순위 | 영역 | 파일 | 영문 문자 | 영어 전용 | 혼합 |",
        "|---:|---|---|---:|---:|---:|",
    ])
    for index, item in enumerate(top_files, 1):
        lines.append(
            f"| {index} | {CATEGORY_LABELS.get(str(item['category']), str(item['category']))} | "
            f"`{item['path']}` | {int(item['english_chars']):,} | "
            f"{int(item['english_only']):,} | {int(item['mixed']):,} |"
        )

    lines.extend([
        "",
        "## 해석 기준",
        "",
        "- `영어 전용`: 한글 없이 의미 있는 영문 단어가 남은 화면 문자열",
        "- `혼합`: 한글과 의미 있는 영문 단어가 함께 있는 문자열. 고유명사일 수도 있으므로 검토 큐로 사용",
        "- `한글`: 한글이 있고 의미 있는 영문 단어가 없는 문자열",
        "- `일본어 후보`: 히라가나/가타카나가 남은 문자열",
        "- HP/MP/STA/EXP 같은 짧은 약어와 일부 도메인 고유어는 영문 잔량 계산에서 제외",
        "",
    ])
    return "\n".join(lines)


def run_self_test() -> None:
    samples = [
        ("PRINTFORML [999] 돌아가기", "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "korean_only", "ui_menu"),
        ("PRINTFORML [999] Return", "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "english_only", "ui_menu"),
        ("PRINTFORML ＜N/A＞", "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "english_only", "ui_menu"),
        ('HTML = "m"', "ERB/TRANSLATION/OMOGATARI/BetterUI.ERB", "english_only", "ui_menu"),
        ("PRINTFORML %AttachmentDisplayName(0, GetAttachmentType(TD_SubPage), ITEM_PICKED)%을(를) 개발했다!", "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "korean_only", "ui_menu"),
        ('HTML = @"Blood {(MAX(0,BASE:ARG:Blood)*100)/MAX(1,MAXBASE:ARG:Blood)}\\%"', "ERB/TRANSLATION/OMOGATARI/BetterUI.ERB", "english_only", "ui_menu"),
        ('HTML = @"혈액 {(MAX(0,BASE:ARG:Blood)*100)/MAX(1,MAXBASE:ARG:Blood)}\\%"', "ERB/TRANSLATION/OMOGATARI/BetterUI.ERB", "korean_only", "ui_menu"),
        ('PRINTL 카리스마(Charisma) 100 기부', "ERB/TRANSLATION/OMOGATARI/ITEM/Item Modding.ERB", "mixed", "ui_menu"),
        ('HTML = DT_CELL_GET(LOCAL, "Hediff Type")', "ERB/TRANSLATION/OMOGATARI/BetterUI.ERB", None, None),
        ('; PRINTL This is a comment', "ERB/TRANSLATION/TEST.ERB", None, None),
        ('PRINTL This is a deliberately long item description that should be categorized as an item description because it is well over one hundred characters and remains visible to the player.', "ERB/TRANSLATION/OMOGATARI/ITEM/Test.ERB", "english_only", "item_description"),
        ('HTML = "This character is brave and receives a bonus when facing danger."', "ERB/TRANSLATION/HTML_TALENTS/HTML_MOUSEOVER.ERB", "english_only", "help_tooltip"),
    ]
    for line, path, expected_state, expected_category in samples:
        strings = extract_strings(line)
        if expected_state is None:
            assert strings == [], (line, strings)
            continue
        assert strings, line
        normalized = normalize_for_language(strings[0])
        state, *_ = classify_state(normalized)
        category = classify_category(path, strings[0], line)
        assert state == expected_state, (line, state, expected_state)
        assert category == expected_category, (line, category, expected_category)
    print("self-test: ok")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="Original/source checkout root")
    parser.add_argument("--target", type=Path, help="Korean checkout root")
    parser.add_argument("--source-ref", default="main")
    parser.add_argument("--target-ref", default="korean")
    parser.add_argument("--output-dir", type=Path, default=Path("translation-progress-v2"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return 0
    if not args.source or not args.target:
        parser.error("--source and --target are required unless --self-test is used")

    source_units = scan_tree(args.source)
    target_units = scan_tree(args.target)
    source_metrics = aggregate(source_units)
    target_metrics = aggregate(target_units)
    rows = rows_for_report(source_metrics, target_metrics)
    top_files = top_remaining_files(target_units)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    markdown = make_markdown(
        args.source_ref,
        args.target_ref,
        source_metrics,
        target_metrics,
        rows,
        top_files,
    )
    (args.output_dir / "summary.md").write_text(markdown, encoding="utf-8")
    write_csv(args.output_dir / "categories.csv", rows)

    payload = {
        "version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_ref": args.source_ref,
        "target_ref": args.target_ref,
        "metric": "meaningful_english_character_reduction",
        "categories": rows,
        "source_total": asdict(total_metrics(source_metrics)),
        "target_total": asdict(total_metrics(target_metrics)),
        "top_remaining_files": top_files,
        "top_english_only": top_review_units(target_units, "english_only"),
        "top_mixed": top_review_units(target_units, "mixed"),
    }
    (args.output_dir / "report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(markdown)
    github_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_summary:
        with open(github_summary, "a", encoding="utf-8") as f:
            f.write(markdown)
            f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
