import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage.classify import classify


class TestClassify(unittest.TestCase):
    def test_bats_is_test(self):
        b, _ = classify("not ok |N| podman healthcheck")
        self.assertEqual(b, "test")

    def test_make_gate_is_designed(self):
        b, _ = classify("make: *** [TARGET] Error 1")
        self.assertEqual(b, "designed")

    def test_arch_mismatch_is_infra(self):
        b, _ = classify("", raw="retrieved architecture x86_64 does not match target architecture arm64")
        self.assertEqual(b, "infra")

    def test_missing_log_is_no_log(self):
        b, _ = classify(None)
        self.assertEqual(b, "no-log")

    def test_unmatched_is_unknown_not_guessed(self):
        b, _ = classify("")
        self.assertEqual(b, "unknown")


if __name__ == "__main__":
    unittest.main()


class TestCheck(unittest.TestCase):
    def test_bats_paste_normalises_to_the_stored_signature(self):
        from flaketriage.check import _norm
        pasted = "not ok 212 |220| podman healthcheck in 15635ms"
        stored = "not ok |N| podman healthcheck"
        self.assertEqual(_norm(pasted), _norm(stored))

    def test_unrelated_test_does_not_match(self):
        from flaketriage.check import _norm, _score
        self.assertLess(_score(_norm("podman network reload"),
                               _norm("podman healthcheck")), 0.55)

    def test_exact_name_scores_above_partial(self):
        from flaketriage.check import _norm, _score
        exact = _score(_norm("podman healthcheck"), _norm("not ok |N| podman healthcheck"))
        partial = _score(_norm("podman healthcheck"),
                         _norm("not ok |N| podman kube play healthcheck should wait"))
        self.assertGreater(exact, partial)
