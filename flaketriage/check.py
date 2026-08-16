"""answer the one question REVIEWING.md actually asks a reviewer.

    "check to see if those tests failed due to known flakes"

Paste the failing test name, get back whether this project has seen it flake,
how often, when it last happened, and on which jobs.
"""

import re

from . import ingest


def _norm(s):
    """lowercase, collapse whitespace, drop the bats numbering noise so a
    pasted 'not ok 212 |220| podman healthcheck' matches the stored sig."""
    s = s.lower()
    # bats prefixes come in two shapes: raw from a log ("not ok 212 |220| ")
    # and already normalised by extract ("not ok |N| "). strip both.
    s = re.sub(r"^\s*(not ok|ok)\b\s*\d*\s*", "", s)
    s = re.sub(r"\|[^|]{0,6}\|", " ", s)
    s = re.sub(r"\bin \d+ms\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def _score(needle, hay):
    """cheap containment score - no dependencies, and precision matters more
    than recall here because a wrong 'known flake' answer is worse than none."""
    if not needle:
        return 0.0
    if needle == hay:
        return 1.0
    if needle in hay:
        return 0.9
    nw, hw = set(needle.split()), set(hay.split())
    if not nw:
        return 0.0
    return len(nw & hw) / len(nw) * 0.8


def check(query, limit=5, log=print):
    st = ingest.load_state()
    flakes = st.get("flakes") or []
    if not flakes:
        log("no corpus yet - run scan first")
        return 1

    needle = _norm(query)
    seen = {}
    for f in flakes:
        sig = f.get("sig") or ""
        if not sig or sig == "(no log / no marker)":
            continue
        s = _score(needle, _norm(sig))
        if s < 0.55:
            continue
        e = seen.setdefault(sig, {"n": 0, "score": s, "dates": [], "jobs": set()})
        e["n"] += 1
        e["score"] = max(e["score"], s)
        if f.get("date"):
            e["dates"].append(f["date"])
        if f.get("job"):
            e["jobs"].add(f["job"])

    if not seen:
        log(f'no flake on record matching "{query}"')
        log("")
        log("that is not the same as 'not a flake'. it means this project has not")
        log("re-run and passed this test since the corpus began. treat the failure")
        log("as real until something says otherwise.")
        return 0

    ranked = sorted(seen.items(), key=lambda kv: (-kv[1]["score"], -kv[1]["n"]))[:limit]
    total = len(st.get("runs") or {})

    for sig, e in ranked:
        dates = sorted(e["dates"])
        log("")
        log(f"  {sig}")
        log(f"  seen {e['n']}x across {total} runs, {dates[0]} to {dates[-1]}")
        log(f"  jobs: {', '.join(sorted(e['jobs'])[:4])}")
        if e["score"] < 0.9:
            log("  (partial name match - confirm this is the same test)")
    log("")
    log("known flake means it failed and later passed on the same commit.")
    log("it does not mean this particular failure is safe to ignore.")
    return 0
