"""Second oracle: recognise a known flake in a run nobody re-ran.

The rerun oracle in ingest.py only sees a failure once a maintainer has
clicked re-run. Measured on this corpus that is 28% of runs, so roughly
seven out of ten runs are invisible to it - a job failed once, irritated
somebody, and got papered over by a push.

This module covers part of that gap without needing a re-run. If a failure
signature has already been *proven* flaky by a maintainer's own re-run
somewhere else, then the same signature appearing in a run nobody re-ran is
the same known flake showing up again. The evidence is weaker than the rerun
oracle - there is no passing twin of that exact job to diff against - so
these are recorded with oracle="corroborated" and are never mixed into the
rerun-confirmed counts.

Two guards matter, and both cost real accuracy if dropped:

  1. Only signatures confirmed by the *rerun* oracle seed this. A
     corroborated flake never corroborates another one, so a single wrong
     match cannot spread through the corpus.
  2. Signatures that classify as "designed" are excluded. podman's
     tests-included gate fails on purpose until a maintainer applies a
     label; it is the single most frequent signature in the corpus and
     labelling every one of its instances a flake would be wrong.

What this still cannot see: a failure whose signature has never once been
re-run to green, and anything with no framework marker at all.
"""
import re

from . import gh
from .classify import classify
from .extract import INFRA_LINES, MARKERS, normalise
from .ingest import load_state, save_state

# a rerun-confirmed flake carries no oracle field in corpora written before
# this module existed; treat those as the rerun oracle they came from
RERUN = "rerun"
CORROBORATED = "corroborated"


def oracle_of(flake):
    return flake.get("oracle", RERUN)


def confirmed_signatures(st):
    """Signatures the rerun oracle has proven, minus the designed failures.

    Returns {signature: number of distinct runs it was confirmed in}. The
    count is kept because a signature confirmed across several independent
    runs is much stronger evidence than one confirmed once.
    """
    runs_per_sig = {}
    for f in st["flakes"]:
        if oracle_of(f) != RERUN:
            continue
        sig = f.get("sig")
        if not sig:
            continue
        if classify(sig, f.get("raw", ""))[0] == "designed":
            continue
        runs_per_sig.setdefault(sig, set()).add(f["run_id"])
    return {sig: len(runs) for sig, runs in runs_per_sig.items()}


def signature_of(text):
    """The failure line for a log, using framework markers only.

    Same rule as extract.py: never a bare grep for "Error", because podman's
    negative tests print expected errors that a naive grep reads as failures.
    """
    for pat in MARKERS + INFRA_LINES:
        m = re.search(pat, text)
        if m:
            raw = m.group(0)[:300]
            return raw, normalise(raw)
    return "", ""


def corroborate(limit=None, created=None, min_runs=1, log=print):
    """Walk runs that were never re-run and match their failures to known flakes.

    min_runs raises the bar on the seeding side: with min_runs=2 only
    signatures the rerun oracle confirmed in two or more distinct runs are
    allowed to corroborate anything.
    """
    st = load_state()
    repo, wf = st.get("repo"), st.get("workflow")
    if not repo:
        raise SystemExit("no corpus yet - run scan first")

    known = {s: n for s, n in confirmed_signatures(st).items() if n >= min_runs}
    log(f"{len(known)} rerun-confirmed signatures eligible to corroborate")
    if not known:
        return st

    seen = {(f["run_id"], f["job_id"]) for f in st["flakes"]}
    wid = _workflow_id(repo, wf)
    path = f"repos/{repo}/actions/workflows/{wid}/runs?status=completed"
    if created:
        path += f"&created={created}"

    scanned = added = nolog = 0
    for run in gh.paginate(path, "workflow_runs"):
        rid = str(run["id"])
        entry = st["runs"].get(rid)
        # only runs the rerun oracle cannot help with, and only failing ones
        if run["run_attempt"] > 1 or run["conclusion"] != "failure":
            continue
        if entry and entry.get("corr"):
            continue  # incremental: already corroborate-scanned
        if limit and scanned >= limit:
            break
        scanned += 1

        for job in gh.paginate(f"repos/{repo}/actions/runs/{rid}/jobs", "jobs"):
            if job["conclusion"] != "failure":
                continue
            # aggregate gate jobs go red whenever any real job does
            if job["name"].lower().startswith("total "):
                continue
            if (rid, str(job["id"])) in seen:
                continue
            text = gh.api_text(f"repos/{repo}/actions/jobs/{job['id']}/logs")
            if not text or len(text) < 1000:
                nolog += 1
                continue
            raw, sig = signature_of(text)
            if not sig or sig not in known:
                continue
            st["flakes"].append(
                {
                    "run_id": rid,
                    "job_id": str(job["id"]),
                    "job": job["name"],
                    "date": run["created_at"][:10],
                    "raw": raw,
                    "sig": sig,
                    "oracle": CORROBORATED,
                    "confirmed_in_runs": known[sig],
                }
            )
            seen.add((rid, str(job["id"])))
            added += 1

        st["runs"].setdefault(rid, {"attempts": run["run_attempt"], "created": run["created_at"][:10]})
        st["runs"][rid]["corr"] = True
        if scanned % 10 == 0:
            save_state(st)
            log(f"  {scanned} never-rerun failing runs scanned, {added} corroborated")

    save_state(st)
    log(
        f"done: {scanned} never-rerun failing runs scanned, "
        f"{added} corroborated flakes added, {nolog} jobs had no retrievable log"
    )
    return st


def _workflow_id(repo, wf_file):
    for w in (gh.api(f"repos/{repo}/actions/workflows") or {}).get("workflows", []):
        if w["path"].endswith("/" + wf_file):
            return w["id"]
    raise SystemExit(f"workflow {wf_file} not found in {repo}")


def summary(st=None):
    """Counts per oracle, so the two are never reported as one number."""
    st = st or load_state()
    out = {RERUN: 0, CORROBORATED: 0}
    for f in st["flakes"]:
        out[oracle_of(f)] = out.get(oracle_of(f), 0) + 1
    return out
