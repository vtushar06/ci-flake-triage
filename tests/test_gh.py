"""Pins the log-fetch contract.

The corpus lost two weeks of signatures because a 403 from the log endpoint
was recorded as "no retrievable log". A log we are not allowed to read and a
log that does not exist are different facts and must not share a return value.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage import gh


class _Result:
    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class GhStub(unittest.TestCase):
    def stub(self, returncode, stdout="", stderr=""):
        real = gh.subprocess.run
        self.addCleanup(setattr, gh.subprocess, "run", real)
        gh.subprocess.run = lambda *a, **k: _Result(returncode, stdout, stderr)


class TestApiText(GhStub):
    PATH = "repos/o/r/actions/jobs/1/logs"

    def test_success_returns_the_log(self):
        self.stub(0, stdout="not ok 212 |220| podman healthcheck\n")
        self.assertIn("not ok 212", gh.api_text(self.PATH))

    def test_missing_log_returns_none(self):
        # a superseded attempt really does have no log - that is a fact, keep it
        self.stub(1, stderr="gh: Not Found (HTTP 404)")
        self.assertIsNone(gh.api_text(self.PATH))

    def test_expired_log_returns_none(self):
        self.stub(1, stderr="gh: Gone (HTTP 410)")
        self.assertIsNone(gh.api_text(self.PATH))

    def test_permission_failure_raises(self):
        # what CI actually hit: the workflow token cannot read another repo's
        # job logs, and the whole corpus quietly filled up with "no log"
        self.stub(1, stderr="gh: Resource not accessible by integration (HTTP 403)")
        with self.assertRaises(gh.ApiError):
            gh.api_text(self.PATH)

    def test_server_error_raises(self):
        self.stub(1, stderr="gh: Server Error (HTTP 502)")
        with self.assertRaises(gh.ApiError):
            gh.api_text(self.PATH)


if __name__ == "__main__":
    unittest.main()
