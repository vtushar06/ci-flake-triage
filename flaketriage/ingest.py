"""Find confirmed flakes in a workflow's rerun history.

A confirmed flake: a job that failed on one attempt and passed on a later
attempt of the SAME run. The commit is identical across attempts, so the
failure cannot have been the code. Every manual re-run in the history is a
maintainer saying "I think that failure was not real" - that human judgement
is the ground truth here, and it needs no change to the CI under test.

State lives in data/corpus.json and is incremental: runs already processed
are never fetched again, so after the first full pass a daily run only
touches the new runs.
"""
import json
import os

from . import gh

STATE = os.path.join(os.path.dirname(__file__), "..", "data", "corpus.json")


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"repo": None, "workflow": None, "runs": {}, "flakes": []}


def save_state(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    tmp = STATE + ".tmp"
    json.dump(st, open(tmp, "w"), indent=1)
    os.replace(tmp, STATE)


def workflow_id(repo, wf_file):
    for w in (gh.api(f"repos/{repo}/actions/workflows") or {}).get("workflows", []):
        if w["path"].endswith("/" + wf_file):
            return w["id"]
    raise SystemExit(f"workflow {wf_file} not found in {repo}")


def scan(repo, wf_file, limit=None, created=None, log=print):
    """Walk completed runs newest-first, diff attempts on re-run ones.

    The runs listing is capped at about 1000 results per query, so one pass
    cannot see a history longer than that. Pass created="YYYY-MM-DD..YYYY-MM-DD"
    to scan an older window; state is keyed by run id, so overlapping windows
    are harmless and a few backfill passes cover any history.
    """
    st = load_state()
    if st["repo"] and st["repo"] != repo:
        raise SystemExit(
            f"state in {STATE} is for {st['repo']}; delete it to scan {repo}"
        )
    st["repo"], st["workflow"] = repo, wf_file
    wid = workflow_id(repo, wf_file)
    seen_flakes = {(f["run_id"], f["job_id"]) for f in st["flakes"]}
    processed = 0

    path = f"repos/{repo}/actions/workflows/{wid}/runs?status=completed"
    if created:
        path += f"&created={created}"
    for run in gh.paginate(path, "workflow_runs"):
        rid = str(run["id"])
        if limit and processed >= limit:
            break
        prev = st["runs"].get(rid)
        if prev and prev["attempts"] >= run["run_attempt"]:
            continue  # incremental: already done at this attempt count
        # a run seen earlier at a lower attempt count was re-run since -
        # skipping it here would lose its flakes for good
        processed += 1
        entry = {"attempts": run["run_attempt"], "created": run["created_at"][:10]}

        if run["run_attempt"] > 1:
            # jobs that failed on any earlier attempt... A None from the API
            # here means the attempt data is gone (404); an outage raises
            # inside gh.api instead, so this run is not recorded as done.
            failed = {}
            for a in range(1, run["run_attempt"]):
                jobs = list(
                    gh.paginate(f"repos/{repo}/actions/runs/{rid}/attempts/{a}/jobs", "jobs")
                )
                for j in jobs:
                    if j["conclusion"] == "failure":
                        failed[j["name"]] = j["id"]
            # ...and passed on the final one. Aggregate jobs ("Total Success"
            # style) fail whenever any real job fails, so they double-count.
            if failed:
                final = {
                    j["name"]: j["conclusion"]
                    for j in gh.paginate(
                        f"repos/{repo}/actions/runs/{rid}/attempts/{run['run_attempt']}/jobs",
                        "jobs",
                    )
                }
                for name, jid in failed.items():
                    if final.get(name) != "success" or name.lower().startswith("total "):
                        continue
                    if (rid, jid) in seen_flakes:
                        continue
                    st["flakes"].append(
                        {
                            "run_id": rid,
                            "job_id": jid,
                            "job": name,
                            "date": run["created_at"][:10],
                        }
                    )
        st["runs"][rid] = entry
        if processed % 25 == 0:
            save_state(st)
            log(f"  {processed} new runs processed, {len(st['flakes'])} flakes total")

    save_state(st)
    log(
        f"done: {len(st['runs'])} runs in state, "
        f"{sum(1 for r in st['runs'].values() if r['attempts'] > 1)} were re-run, "
        f"{len(st['flakes'])} confirmed flakes"
    )
    return st
