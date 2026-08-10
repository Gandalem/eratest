from __future__ import annotations

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
            if ENG_RE.search(value) and not HANGUL_RE.search(value):
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
            if ENG_RE.search(value) and not HANGUL_RE.search(value):
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


def main() -> None:
    root = Path(".")
    show_structured(root)
    show_trlib(root)


if __name__ == "__main__":
    main()
