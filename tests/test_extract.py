import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage.extract import MARKERS, normalise

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def first_marker(text):
    for pat in MARKERS:
        m = re.search(pat, text)
        if m:
            return m.group(0)
    return ""


class TestMarkers(unittest.TestCase):
    def _fixture(self, name):
        with open(os.path.join(FIX, name)) as f:
            return f.read()

    def test_bats_failure_found(self):
        got = first_marker(self._fixture("bats_healthcheck.log"))
        self.assertTrue(got.startswith("not ok 212"))

    def test_ginkgo_failure_found(self):
        got = first_marker(self._fixture("ginkgo_prune.log"))
        self.assertIn("[FAIL]", got)

    def test_make_gate_found(self):
        got = first_marker(self._fixture("make_gate.log"))
        self.assertIn("make: ***", got)

    def test_expected_error_is_not_a_marker(self):
        # a negative test printing "Error:" must never produce a signature -
        # a greedy grep once invented a top flake out of exactly this log
        got = first_marker(self._fixture("negative_test_trap.log"))
        self.assertEqual(got, "")


class TestNormalise(unittest.TestCase):
    def test_bats_volatile_parts(self):
        a = normalise("not ok 212 |220| podman healthcheck in 15635ms")
        b = normalise("not ok 47 |220| podman healthcheck in 9008ms")
        self.assertEqual(a, b)
        self.assertEqual(a, "not ok |N| podman healthcheck")

    def test_hashes_and_ips(self):
        s = normalise("[FAIL] x cannot bind tcp 10.88.0.2:41545 id deadbeefdeadbeef")
        self.assertNotIn("41545", s)
        self.assertNotIn("10.88.0.2", s)
        self.assertNotIn("deadbeef", s)

    def test_make_target_collapsed(self):
        s = normalise("make: *** [Makefile:775: tests-included] Error 1")
        self.assertEqual(s, "make: *** [TARGET] Error 1")


if __name__ == "__main__":
    unittest.main()
