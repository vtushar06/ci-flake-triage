import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage.attemptdiff import diff
from flaketriage.model import parse_verdict

CAUSES = {"race": "", "infra": "", "unknown": ""}


class TestVerdictParsing(unittest.TestCase):
    def test_valid_json_accepted(self):
        v = parse_verdict('{"cause": "race", "confidence": "high", "deciding_line": "x"}', CAUSES)
        self.assertEqual(v["cause"], "race")

    def test_prose_wrapped_json_accepted(self):
        v = parse_verdict('Sure! Here is my answer: {"cause": "infra", "confidence": "low", "deciding_line": ""} hope that helps', CAUSES)
        self.assertEqual(v["cause"], "infra")

    def test_invalid_label_becomes_unknown(self):
        v = parse_verdict('{"cause": "gremlins", "confidence": "high", "deciding_line": ""}', CAUSES)
        self.assertEqual(v["cause"], "unknown")
        self.assertEqual(v["note"], "invalid label")

    def test_garbage_becomes_unknown_not_crash(self):
        v = parse_verdict("I cannot answer that", CAUSES)
        self.assertEqual(v["cause"], "unknown")


class TestAttemptDiff(unittest.TestCase):
    def test_unique_failing_lines_survive_shared_noise(self):
        fail = "2026-01-01T00:00:00.0Z shared setup\n2026-01-01T00:00:01.0Z not ok 5 |100| t\n2026-01-01T00:00:02.0Z unlinkat /x: read-only file system\n"
        ok = "2026-01-01T00:00:00.0Z shared setup\n2026-01-01T00:00:01.0Z ok 5 |100| t\n"
        lines = diff(fail, ok)
        self.assertTrue(any("read-only file system" in l for l in lines))
        self.assertFalse(any("shared setup" in l for l in lines))

    def test_missing_pass_log_yields_everything_marked(self):
        lines = diff("2026-01-01T00:00:01.0Z not ok 5 |100| t\n", "")
        self.assertTrue(lines)


if __name__ == "__main__":
    unittest.main()
