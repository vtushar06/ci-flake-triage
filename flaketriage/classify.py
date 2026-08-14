"""Sort signatures into cause buckets with plain rules first.

Every rule here earned its place from a real instance in the corpus, and
the buckets are the ones that changed what a maintainer would do with the
report:

  test      - a test-level failure with a framework marker; the thing most
              people mean by "flake"
  designed  - fails on purpose until a human acts (the tests-included gate
              looked like the number-two flake in the corpus until one log
              was opened: it fails by design when a PR has no tests, then a
              maintainer labels and re-runs)
  infra     - the machine, not the test: runner arch mismatch, mirror
              failures, VM bring-up
  no-log    - conclusion=failure but no log survives; a categoriser must
              count these, not guess
  unknown   - everything else, listed loudest: these are exactly the ones
              a human must open

An optional local-model hook can take a shot at "unknown" blocks, but it
only ever sees a pre-extracted snippet and its answer lands in a separate
field - rules are never overridden by a model guess.
"""
import re

RULES = [
    ("designed", r"make: \*\*\* \[TARGET\] Error", "make gates fail by design until a human acts; verify per instance"),
    ("infra", r"retrieved architecture .* does not match", "runner handed out the wrong arch"),
    ("infra", r"(Could not connect to .*mirror|apt.*Connection failed|Temporary failure resolving)", "package mirror or DNS"),
    ("infra", r"(limactl|lima).*(timed out|failed to start)", "CI VM bring-up"),
    ("test", r"^(not ok |#\| FAIL:|\[FAIL\] )", "framework-reported test failure"),
]


def classify(sig, raw=""):
    if sig is None:
        return "no-log", "no retrievable log"
    text = sig or raw
    if not text:
        return "unknown", "no framework marker matched"
    for bucket, pat, why in RULES:
        if re.search(pat, text):
            return bucket, why
    return "unknown", "no rule matched"


def classify_all(state):
    for f in state["flakes"]:
        f["bucket"], f["why"] = classify(f.get("sig"), f.get("raw", ""))
    return state
