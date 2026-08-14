"""Diff the failing attempt's log against the passing attempt's log.

Every confirmed flake gives us both, for the same job on the same commit -
a control group nothing else in the survey had. Races, infra blips and
network timeouts separate here deterministically, before any model runs:
a line class present only in the failing run is signal; everything the two
runs share is noise.
"""
import difflib
import re

from . import gh
from .extract import normalise
from .ingest import load_state


def _lines(text):
    out = []
    for l in text.splitlines():
        l = l.split("Z ", 1)[-1]          # strip the actions timestamp
        l = normalise(l)
        if l:
            out.append(l)
    return out


def fetch_pair(job_id):
    """Return (fail_text, pass_text, flake) for a corpus flake."""
    st = load_state()
    repo = st["repo"]
    flake = next((f for f in st["flakes"] if str(f["job_id"]) == str(job_id)), None)
    if not flake:
        return None, None, None
    fail = gh.api_text(f"repos/{repo}/actions/jobs/{flake['job_id']}/logs")
    run = gh.api(f"repos/{repo}/actions/runs/{flake['run_id']}")
    if not run:
        return fail, None, flake
    final = run["run_attempt"]
    jobs = list(
        gh.paginate(f"repos/{repo}/actions/runs/{flake['run_id']}/attempts/{final}/jobs", "jobs")
    )
    twin = next((j for j in jobs if j["name"] == flake["job"]), None)
    ok = gh.api_text(f"repos/{repo}/actions/jobs/{twin['id']}/logs") if twin else None
    return fail, ok, flake


MARKER = re.compile(r"not ok [0-9]+ |#\| FAIL: |\[FAIL\] |make: \*\*\* ")

NOISE = re.compile(
    r"runner name|machine name|git config|##\[|hostagent|ssh local port|"
    r"downloaded the image|decompressing|qemu|ovmf|guest agent",
    re.I,
)


def diff(fail_text, pass_text, max_lines=40, window=400):
    """Lines unique to the failing run, anchored around the failure.

    Diffing whole logs drowns the signal in per-machine setup noise
    (runner names, VM boot, git plumbing) - measured on a real flake, the
    first 60 unique lines were all setup. So: the passing log contributes
    its full line set for membership, but candidate lines come only from a
    window around the failure marker in the failing log, with known
    infrastructure chatter dropped.
    """
    fl, pl = _lines(fail_text or ""), _lines(pass_text or "")
    passing = set(pl)
    idx = next((i for i, l in enumerate(fl) if MARKER.search(l)), None)
    if idx is not None:
        fl = fl[max(0, idx - window): idx + 40]
    seen, only_fail = set(), []
    for l in fl:
        if l in passing or l in seen or NOISE.search(l):
            continue
        seen.add(l)
        only_fail.append(l)
    only_fail = [l for l in only_fail if not re.fullmatch(r"[<>A-Z0-9_ :.\-]+", l)]
    return only_fail[-max_lines:]


def render(job_id, log=print):
    fail, ok, flake = fetch_pair(job_id)
    if not flake:
        log(f"job {job_id} is not in the corpus")
        return None
    if not fail:
        log("failing log is no longer available")
        return None
    if not ok:
        log("passing attempt log is no longer available - showing nothing rather than guessing")
        return None
    lines = diff(fail, ok)
    log(f"{len(lines)} lines appear only in the failing attempt of {flake['job']}:")
    for l in lines:
        log(f"  {l[:160]}")
    return lines
