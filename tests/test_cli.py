"""A failed API call is a message and an exit code, never a traceback."""
import contextlib
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage import cli, extract, gh


class TestApiErrorReporting(unittest.TestCase):
    def setUp(self):
        real_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", real_argv)
        sys.argv = ["flaketriage", "extract"]
        real = extract.extract_all
        self.addCleanup(setattr, extract, "extract_all", real)

        def boom(*a, **k):
            raise gh.ApiError("gh api repos/o/r/actions/jobs/1/logs failed: HTTP 403")

        extract.extract_all = boom

    def test_exits_nonzero(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(), 1)

    def test_says_what_failed(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            cli.main()
        self.assertIn("403", out.getvalue())


if __name__ == "__main__":
    unittest.main()
