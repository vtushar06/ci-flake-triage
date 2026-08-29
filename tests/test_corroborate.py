import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from flaketriage.corroborate import (
    CORROBORATED,
    RERUN,
    confirmed_signatures,
    oracle_of,
    signature_of,
    summary,
)

HEALTHCHECK = "not ok |N| podman healthcheck"
MAKE_GATE = "make: *** [TARGET] Error 1"


def flake(sig, run_id="1", oracle=None, raw=""):
    f = {"run_id": run_id, "job_id": "j", "job": "sys", "date": "2026-08-01", "sig": sig, "raw": raw}
    if oracle:
        f["oracle"] = oracle
    return f


class TestOracleOf(unittest.TestCase):
    def test_missing_field_means_rerun(self):
        # corpora written before this module have no oracle field at all
        self.assertEqual(oracle_of({"sig": HEALTHCHECK}), RERUN)

    def test_explicit_field_wins(self):
        self.assertEqual(oracle_of(flake(HEALTHCHECK, oracle=CORROBORATED)), CORROBORATED)


class TestConfirmedSignatures(unittest.TestCase):
    def test_counts_distinct_runs_not_instances(self):
        st = {"flakes": [flake(HEALTHCHECK, "1"), flake(HEALTHCHECK, "1"), flake(HEALTHCHECK, "2")]}
        self.assertEqual(confirmed_signatures(st), {HEALTHCHECK: 2})

    def test_designed_failures_are_excluded(self):
        # the tests-included gate fails on purpose; it is the most frequent
        # signature in the corpus and must never seed a corroboration
        st = {"flakes": [flake(MAKE_GATE, "1"), flake(HEALTHCHECK, "2")]}
        self.assertEqual(confirmed_signatures(st), {HEALTHCHECK: 1})

    def test_corroborated_flakes_do_not_seed(self):
        # otherwise one wrong match spreads through the corpus
        st = {"flakes": [flake(HEALTHCHECK, "1", oracle=CORROBORATED)]}
        self.assertEqual(confirmed_signatures(st), {})

    def test_signature_less_flakes_are_skipped(self):
        st = {"flakes": [flake(None, "1"), flake("", "2")]}
        self.assertEqual(confirmed_signatures(st), {})


class TestSignatureOf(unittest.TestCase):
    def test_bats_marker(self):
        raw, sig = signature_of("some noise\nnot ok 212 |220| podman healthcheck in 15635ms\nmore")
        self.assertIn("podman healthcheck", sig)
        self.assertNotIn("212", sig)

    def test_ginkgo_marker(self):
        _, sig = signature_of("[FAIL] Podman rmi [It] podman image rm - concurrent")
        self.assertTrue(sig.startswith("[FAIL] Podman rmi"))

    def test_no_marker_yields_nothing(self):
        # a log with only an expected error from a negative test must not
        # produce a signature - that was a real bug in an earlier version
        self.assertEqual(signature_of("Error: container not known\nError: no such image"), ("", ""))


class TestSummary(unittest.TestCase):
    def test_counts_are_kept_separate(self):
        st = {
            "flakes": [
                flake(HEALTHCHECK, "1"),
                flake(HEALTHCHECK, "2", oracle=CORROBORATED),
                flake(HEALTHCHECK, "3", oracle=CORROBORATED),
            ]
        }
        self.assertEqual(summary(st), {RERUN: 1, CORROBORATED: 2})


if __name__ == "__main__":
    unittest.main()
