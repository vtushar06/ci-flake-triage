"""Fetch the systemd journal artifact for a flake's job.

The reason this module exists at all: the job log can point the wrong way.
The most frequent signature in the corpus got a wrong first diagnosis from
its job log; the journal artifact showed the event the test waits for
firing 19-60 ms before the test starts listening. Any diagnosis that
matters gets checked against the journal, so fetching one should be one
command, not five API calls done by hand.
"""
import io
import os
import zipfile

from . import gh
from .ingest import STATE, load_state

JOURNALS = os.path.join(os.path.dirname(STATE), "journals")


def _artifact_names(job_name):
    # "sys local rootless debian-sid / lima" -> the artifact holding its journal.
    # Upstream renamed these in early August 2026, so both shapes exist in the
    # history: "journal-<job>.log" before, "<job>.logs" after.
    base = job_name.split(" / ")[0].replace(" ", "-")
    return [f"journal-{base}.log", f"{base}.logs"]


def fetch(job_id, log=print):
    """Download the journal for one corpus flake. Returns the local path."""
    st = load_state()
    repo = st["repo"]
    flake = next((f for f in st["flakes"] if str(f["job_id"]) == str(job_id)), None)
    if not flake:
        log(f"job {job_id} is not in the corpus")
        return None

    wanted = _artifact_names(flake["job"])
    arts = gh.api(f"repos/{repo}/actions/runs/{flake['run_id']}/artifacts?per_page=100")
    hits = sorted(
        (a for a in (arts or {}).get("artifacts", []) if a["name"] in wanted),
        key=lambda a: a["created_at"],
    )
    if not hits:
        names = [a["name"] for a in (arts or {}).get("artifacts", [])]
        log(f"no artifact named {' or '.join(wanted)}; artifacts on that run: {names[:8]}")
        return None
    # A re-run leaves two artifacts with the same name on the run - the
    # failing attempt's and the passing re-run's. The flake lives on the
    # early attempt, so take the earliest. Picking the wrong one silently
    # hands you a healthy journal, which is worse than no journal.
    hit = hits[0]
    if len(hits) > 1:
        log(f"{len(hits)} artifacts named {hit['name']}; taking the earliest ({hit['created_at']})")
    if hit.get("expired"):
        log(f"artifact {want} has expired")
        return None

    blob = gh.api_bytes(f"repos/{repo}/actions/artifacts/{hit['id']}/zip")
    if not blob:
        log("download failed")
        return None
    os.makedirs(JOURNALS, exist_ok=True)
    out = os.path.join(JOURNALS, f"{job_id}.log")
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        member = z.namelist()[0]
        with z.open(member) as src, open(out, "wb") as dst:
            dst.write(src.read())
    log(f"wrote {out} ({os.path.getsize(out)} bytes)")
    return out
