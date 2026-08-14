import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage.match import match


class TestMatch(unittest.TestCase):
    ISSUES = [
        {"number": 100, "title": "healthcheck test flakes", "body": "seen often"},
        {"number": 200, "title": "prune race", "body": "log shows: timed out waiting for the external containers to appear here"},
    ]

    def test_verbatim_error_beats_name_similarity(self):
        sigs = {"#| FAIL: timed out waiting for the external containers to appear here": 5}
        rows = match(sigs, self.ISSUES)
        self.assertEqual(rows[0]["issue"], 200)
        self.assertFalse(rows[0]["needs_human"])

    def test_name_only_match_is_flagged_for_a_human(self):
        sigs = {"not ok |N| podman healthcheck": 3}
        rows = match(sigs, self.ISSUES)
        self.assertTrue(all(r["needs_human"] for r in rows))

    def test_no_overlap_yields_nothing(self):
        rows = match({"not ok |N| something else entirely": 1}, self.ISSUES)
        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
