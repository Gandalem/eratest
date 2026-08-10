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
# same variable names. Translate every active display-array definition, not
# only the first definition found by the initial diagnostic.
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
    print('LIST_CHANGED_LINES', changed_lines)
    return ''.join(lines), changed_lines

mod.apply_list = apply_list_all
mod.main()
