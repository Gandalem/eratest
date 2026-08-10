from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

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

mod.main()
