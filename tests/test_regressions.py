"""Each test here pins a bug that adversarial review found before publish."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage.classify import classify
from flaketriage.extract import normalise
from flaketriage.match import match
from flaketriage.report import _shown


class TestRegressions(unittest.TestCase):
    def test_file_line_refs_stay_distinct(self):
        # the port rule used to eat any :NNNN, collapsing different failures
        a = normalise("#| FAIL: command failed at helpers.bash:1234 in setup")
        b = normalise("#| FAIL: command failed at helpers.bash:9876 in setup")
        self.assertNotEqual(a, b)

    def test_ip_ports_still_collapse(self):
        a = normalise("cannot bind tcp 10.88.0.2:41545")
        b = normalise("cannot bind tcp 10.88.0.3:39112")
        self.assertEqual(a, b)

    def test_markdown_injection_is_neutralised(self):
        s = _shown("not ok |N| use `curl` | [x](y) <img>", 200)
        self.assertNotIn("`", s)
        # every pipe must be escaped so a table cell cannot be broken open
        for i, ch in enumerate(s):
            if ch == "|":
                self.assertEqual(s[i - 1], "\\", f"unescaped pipe at {i}: {s!r}")

    def test_generic_one_word_title_does_not_win(self):
        issues = [
            {"number": 1, "title": "healthcheck", "body": ""},
            {"number": 2, "title": "podman healthcheck timeout in container flakes", "body": ""},
        ]
        rows = match({"not ok |N| podman healthcheck timeout in container": 3}, issues)
        self.assertEqual(rows[0]["issue"], 2)

    def test_infra_line_reaches_the_infra_bucket(self):
        b, _ = classify("", raw="Fatal error: retrieved architecture x86_64 does not match target architecture arm64")
        self.assertEqual(b, "infra")


if __name__ == "__main__":
    unittest.main()
