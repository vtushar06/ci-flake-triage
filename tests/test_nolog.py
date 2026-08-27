"""The "no retrievable log" marker is terminal, so only a real absence earns it.

Every flake recorded between 2026-08-14 and 2026-08-26 got this marker from a
token error, not from a missing log, and the marker is what stopped them ever
being read again.
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage import extract, gh, ingest


class StateOnDisk(unittest.TestCase):
    def state(self, flakes):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        self.addCleanup(os.unlink, path)
        real = ingest.STATE
        self.addCleanup(setattr, ingest, "STATE", real)
        ingest.STATE = path
        with open(path, "w") as f:
            json.dump({"repo": "o/r", "workflow": "ci.yml", "runs": {}, "flakes": flakes}, f)
        return path

    def read(self, path):
        with open(path) as f:
            return json.load(f)["flakes"]

    def stub_api_text(self, fn):
        real = gh.api_text
        self.addCleanup(setattr, gh, "api_text", real)
        gh.api_text = fn


class TestExtractOnFetchFailure(StateOnDisk):
    def test_unreadable_log_is_not_recorded_as_missing(self):
        path = self.state([{"run_id": 1, "job_id": 2, "job": "sys local", "date": "2026-08-24"}])

        def boom(_):
            raise gh.ApiError("gh api ... failed: gh: Resource not accessible by integration (HTTP 403)")

        self.stub_api_text(boom)
        with self.assertRaises(gh.ApiError):
            extract.extract_all(log=lambda *a: None)
        f = self.read(path)[0]
        self.assertNotIn("no_log", f)
        self.assertNotIn("sig", f)

    def test_missing_log_is_still_recorded_as_missing(self):
        path = self.state([{"run_id": 1, "job_id": 2, "job": "sys local", "date": "2026-08-24"}])
        self.stub_api_text(lambda _: None)
        extract.extract_all(log=lambda *a: None)
        f = self.read(path)[0]
        self.assertTrue(f["no_log"])


class TestRetryNoLog(StateOnDisk):
    def test_marked_flakes_are_queued_again(self):
        path = self.state([{"run_id": 1, "job_id": 2, "sig": None, "no_log": True}])
        n = extract.retry_no_log(log=lambda *a: None)
        f = self.read(path)[0]
        self.assertEqual(n, 1)
        self.assertNotIn("no_log", f)
        self.assertNotIn("sig", f)

    def test_extracted_flakes_are_left_alone(self):
        path = self.state([{"run_id": 1, "job_id": 2, "sig": "not ok |N| podman healthcheck",
                            "raw": "not ok 212 |220| podman healthcheck"}])
        extract.retry_no_log(log=lambda *a: None)
        f = self.read(path)[0]
        self.assertEqual(f["sig"], "not ok |N| podman healthcheck")


if __name__ == "__main__":
    unittest.main()
