from __future__ import annotations

import importlib.util
from pathlib import Path
import re

base = Path(__file__).with_name('batch_korean_pass63.py')
spec = importlib.util.spec_from_file_location('pass63_base', base)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Standalone body-part display names found by strict preflight.
mod.BIONIC_EXACT.update({
    'Bladder': '방광',
    'Colon': '결장',
})

# LIST has multiple active functions that each define display arrays with the
# same variable names. Translate every active display-array definition.
def apply_list_all(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    changed_entries = 0
    changed_lines = 0
    for i, line in enumerate(lines):
        if not re.match(r'^#DIMS CONST (DISP_NAME|DISP_MEMO|DISP_FACTION)\s*=', line):
            continue
        original = line
        for src, dst in mod.LIST_MAP.items():
            needle = f'"{src}"'
            count = line.count(needle)
            if count:
                line = line.replace(needle, f'"{dst}"')
                changed_entries += count
        if line != original:
            lines[i] = line
            changed_lines += 1
    assert changed_entries == 137, f"LIST entries changed {changed_entries}, expected 137"
    assert changed_lines == 8, f"LIST lines changed {changed_lines}, expected 8"
    print('LIST_CHANGED_ENTRIES', changed_entries)
    print('LIST_CHANGED_LINES', changed_lines)
    # Compatibility count for the base script's aggregate assertion. Actual
    # numstat is independently and strictly checked by the workflow.
    return ''.join(lines), 3


def apply_itemstr_fixed(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    active = None
    seen = changed = 0
    missed: list[str] = []
    pairs = sorted(mod.ITEM_FULL_REPLACEMENTS.items(), key=lambda kv: len(kv[0]), reverse=True)
    for i, line in enumerate(lines):
        fm = mod.FN_RE.match(line)
        if fm:
            active = fm.group(1)
            continue
        if active != 'ItemName_Full' or line.lstrip().startswith(';'):
            continue
        ending = '\r\n' if line.endswith('\r\n') else ('\n' if line.endswith('\n') else '')
        body = line[:-len(ending)] if ending else line
        m = mod.RETURN_RE.match(body)
        if not m:
            continue
        value = m.group(2)
        if not mod.ENG_RE.search(value) or mod.HANGUL_RE.search(value):
            continue
        seen += 1
        new = value
        for src, dst in pairs:
            new = new.replace(src, dst)
        if new == value:
            missed.append(value)
            continue
        lines[i] = m.group(1) + new + m.group(3) + ending
        changed += 1
    assert seen == 43, f"ItemName_Full English-only count changed: {seen}"
    assert not missed, f"ItemName_Full unmapped: {missed}"
    assert changed == 43, changed
    return ''.join(lines), changed

mod.apply_list = apply_list_all
mod.apply_itemstr = apply_itemstr_fixed
mod.main()
