from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_lab",
    ROOT / "scripts" / "validate_lab.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load lab validator")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ManifestTests(unittest.TestCase):
    def test_default_manifest_is_complete(self) -> None:
        MODULE.validate_manifest(ROOT / "lab-manifest.json")

    def test_duplicate_keys_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "manifest.json"
            path.write_text(
                '{"schema":"mindburn.release-permit-adversarial/v1",'
                '"schema":"forged","cases":[]}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                MODULE.validate_manifest(path)


if __name__ == "__main__":
    unittest.main()
