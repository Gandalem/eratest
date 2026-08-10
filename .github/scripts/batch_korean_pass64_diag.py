from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

BOM = b"\xef\xbb\xbf"
ENG_RE = re.compile(r"[A-Za-z]{2,}")
HANGUL_RE = re.compile(r"[가-힣]")
FN_RE = re.compile(r'^@([A-Za-z0-9_]+)(?:\(|$)')
CASE_RE = re.compile(r'^\s*CASE\s+"((?:\\.|[^"\\])*)"')
MAKE_RE = re.compile(r'CALLF\s+MAKE_STR\(V_NAME,\s*@?"((?:\\.|[^"\\])*)"')
STR_RE = re.compile(r'"((?:\\.|[^"\\])*)"')

FILES = {
    "receivers": ("ERB/TRANSLATION/OMOGATARI/ITEM/Armory/Attatchments/Receivers.ERB", {"名前", "ShortName", "描写", "Inspect"}),
    "rifles": ("ERB/TRANSLATION/OMOGATARI/ITEM/Armory/300 Firearms/400 Rifles.ERB", {"名前", "ShortName", "描写", "Inspect"}),
    "melee": ("ERB/TRANSLATION/OMOGATARI/ITEM/Armory/000 Melee/000 Melee.ERB", {"名前", "ShortName", "描写", "Inspect"}),
    "ammo": ("ERB/TRANSLATION/OMOGATARI/ITEM/Armory/Attatchments/Ammunition.ERB", {"名前", "ShortName", "描写", "Inspect"}),
    "bionic": ("ERB/TRANSLATION/OMOGATARI/Body Parts/Bionic List.ERB", {"名前", "FullName", "描写", "Inspect"}),
    "spell": ("ERB/TRANSLATION/OMOGATARI/ITEM/Omogatari_SpellCards.ERB", {"名前", "Name", "FullName", "ShortName", "描写", "Description", "Inspect"}),
}


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(BOM):
        return raw.decode("utf-8-sig")
    return raw.decode("utf-8")


def english_only(value: str) -> bool:
    return bool(ENG_RE.search(value) and not HANGUL_RE.search(value))


def show_structured(root: Path) -> None:
    total = 0
    for key, (rel, allowed) in FILES.items():
        text = read_text(root / rel)
        fn = ""
        field = ""
        count = 0
        print(f"=== FILE {key} :: {rel} ===")
        for lineno, line in enumerate(text.splitlines(), 1):
            fm = FN_RE.match(line)
            if fm:
                fn = fm.group(1)
            cm = CASE_RE.match(line)
            if cm:
                field = cm.group(1)
                continue
            if field not in allowed or line.lstrip().startswith(";"):
                continue
            mm = MAKE_RE.search(line)
            if not mm:
                continue
            value = mm.group(1)
            if english_only(value):
                count += 1
                total += 1
                print(f"C\t{key}\t{lineno}\t{fn}\t{field}\t{value}")
        print(f"COUNT\t{key}\t{count}")
    print(f"STRUCTURED_TOTAL\t{total}")


def show_trlib(root: Path) -> None:
    rel = "ERB/TRANSLATION/_TR Lib.ERB"
    text = read_text(root / rel)
    fn = ""
    counts: dict[str, int] = {}
    rows: list[tuple[str, int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        fm = FN_RE.match(line)
        if fm:
            fn = fm.group(1)
            continue
        if not fn.endswith("_TR") or line.lstrip().startswith(";"):
            continue
        values = STR_RE.findall(line)
        for value in values:
            if english_only(value):
                counts[fn] = counts.get(fn, 0) + 1
                rows.append((fn, lineno, value))
    print("=== TRLIB FUNCTION COUNTS ===")
    for name, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"TRCOUNT\t{name}\t{count}")
    print(f"TRLIB_TOTAL\t{sum(counts.values())}")
    print("=== TRLIB VALUES (functions with <= 80 English literals) ===")
    for fn, lineno, value in rows:
        if counts[fn] <= 80:
            print(f"T\t{lineno}\t{fn}\t{value}")


def show_talent(root: Path) -> None:
    rel = "ERB/TRANSLATION/OMOGATARI/TALENTNAME_NAS.ERB"
    text = read_text(root / rel)
    total = 0
    print("=== TALENTNAME OUTPUT STRINGS ===")
    output_re = re.compile(r'^\s*(?:RETURNF\s+@?|LOCALS(?::\d+)?\s*(?:\'=|\+=)\s*@?)"((?:\\.|[^"\\])*)"')
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(";"):
            continue
        m = output_re.match(line)
        if not m:
            continue
        value = m.group(1)
        if english_only(value):
            total += 1
            print(f"N\t{lineno}\t{value}")
    print(f"TALENT_OUTPUT_TOTAL\t{total}")


def show_list(root: Path) -> None:
    rel = "ERB/TRANSLATION/LIST.ERB"
    text = read_text(root / rel)
    total = 0
    counts = Counter()
    print("=== LIST SCREEN STRINGS ===")
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith(";"):
            continue
        kind = None
        if stripped.startswith("#DIMS CONST"):
            kind = "CONST"
        elif re.match(r'^(?:PRINT|PRINTFORM|PRINTFORML|PRINTFORMS|PRINTBUTTON|PRINTBUTTONC|PRINTBUTTONLC|PRINTBUTTONL|PRINTS|PRINTSL|DRAWLINEFORM)', stripped):
            kind = "PRINT"
        elif stripped.startswith("RETURNF"):
            kind = "RETURN"
        elif re.match(r'^LOCALS(?::\d+)?\s*(?:\'=|\+=)', stripped):
            kind = "LOCALS"
        if not kind:
            continue
        for value in STR_RE.findall(line):
            if english_only(value):
                total += 1
                counts[kind] += 1
                print(f"L\t{lineno}\t{kind}\t{value}")
    print(f"LIST_SCREEN_TOTAL\t{total}\t{dict(counts)}")


def show_ideology(root: Path) -> None:
    rel = "ERB/TRANSLATION/OMOGATARI/Ideology.ERB"
    text = read_text(root / rel)
    field = ""
    counts = Counter()
    rows: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        cm = CASE_RE.match(line)
        if cm:
            field = cm.group(1)
            continue
        if line.lstrip().startswith(";"):
            continue
        mm = MAKE_RE.search(line)
        if not mm:
            continue
        value = mm.group(1)
        if english_only(value):
            counts[field] += 1
            rows.append((lineno, field, value))
    print("=== IDEOLOGY FIELD COUNTS ===")
    for field, count in counts.most_common():
        print(f"ICOUNT\t{field}\t{count}")
    print(f"IDEOLOGY_TOTAL\t{sum(counts.values())}")
    for lineno, field, value in rows:
        if field in {"Name", "Deity", "Description", "Adjective", "MemberName", "LeaderTitle", "FollowerName"}:
            print(f"I\t{lineno}\t{field}\t{value}")


def main() -> None:
    root = Path(".")
    show_structured(root)
    show_trlib(root)
    show_talent(root)
    show_list(root)
    show_ideology(root)


if __name__ == "__main__":
    main()
