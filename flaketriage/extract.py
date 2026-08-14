"""Pull each flake's log and extract the failure using framework markers only.

Never a generic "Error:" grep. Negative tests print expected errors all the
time, and a greedy pattern will hand you a confident, wrong top result -
it produced a fake number-one flake out of a test literally named "bad
machine name" before this rule existed.

Signatures are normalised: timings, sequence numbers and hashes vary per
run and would split one flake into many.
"""
import json
import os
import re

from . import gh
from .ingest import load_state, save_state

# ordered: first match wins
MARKERS = [
    r"not ok [0-9]+ .*",                       # bats
    r"#\| FAIL: .*",                           # bats helper detail
    r"\[FAIL\] .*",                            # ginkgo
    r"make: \*\*\* \[[^\]]*\] Error [0-9]+",   # make targets
]

# When no framework marker matches, the failure is usually the machine, not
# a test. These lines are worth keeping as the raw text so classify can put
# the flake in the infra bucket instead of unknown.
INFRA_LINES = [
    r"retrieved architecture .* does not match.*",
    r"(?:Could not connect to .*mirror|Temporary failure resolving).*",
    r"(?:limactl|lima).*(?:timed out|failed to start).*",
]


def normalise(s):
    s = re.sub(r"\s+in \d+ms$", "", s)
    s = re.sub(r"^not ok \d+ ", "not ok ", s)
    s = re.sub(r"\|\d+\|", "|N|", s)
    s = re.sub(r"\[\d+\]", "[N]", s)
    s = re.sub(r"\b[0-9a-f]{12,64}\b", "<HASH>", s)
    s = re.sub(r"make: \*\*\* \[[^\]]*\]", "make: *** [TARGET]", s)
    s = re.sub(r"\b\d+\.\d+\.\d+\.\d+\b", "<IP>", s)
    # only a port after an address - a bare :NNNN also matches file:line
    # references and would collapse different failures into one signature
    s = re.sub(r"(?<=<IP>):\d{2,5}\b", ":<PORT>", s)
    return s.strip()


def extract_all(log=print):
    st = load_state()
    repo = st["repo"]
    done = no_log = 0
    for f in st["flakes"]:
        if "sig" in f:
            continue
        text = gh.api_text(f"repos/{repo}/actions/jobs/{f['job_id']}/logs")
        if not text or len(text) < 1000:
            # BlobNotFound-class: superseded attempts sometimes have no log
            # at all. Count them, never guess a signature for them.
            f["sig"] = None
            f["no_log"] = True
            no_log += 1
            continue
        raw = ""
        for pat in MARKERS:
            m = re.search(pat, text)
            if m:
                raw = m.group(0)
                break
        if not raw:
            for pat in INFRA_LINES:
                m = re.search(pat, text)
                if m:
                    raw = m.group(0)
                    break
        f["raw"] = raw[:300]
        f["sig"] = normalise(raw) if raw else ""
        done += 1
        if done % 25 == 0:
            save_state(st)
            log(f"  {done} logs extracted")
    save_state(st)
    log(f"done: {done} extracted, {no_log} had no retrievable log")
    return st
