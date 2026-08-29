"""Write the two reports maintainers actually asked for.

The shape comes from a maintainer's own words about what a flake report
should be: the example log failures, the instances, how common it is.
No prose beyond that.

known-flakes.md - every signature, bucketed, with occurrence links and
                  issue-match candidates
weekly.md      - the last 7 days only, small enough to read in a minute
"""
import collections
import datetime
import difflib
import os

from .classify import classify_all
from . import corroborate
from .ingest import STATE, load_state
from . import match as matcher

REPORTS = os.path.join(os.path.dirname(STATE), "..", "reports")


def _groups(st):
    g = collections.defaultdict(list)
    for f in st["flakes"]:
        g[f.get("sig")].append(f)
    return g


def _link(repo, f):
    return f"https://github.com/{repo}/actions/runs/{f['run_id']}/job/{f['job_id']}"


def _today():
    return datetime.datetime.now(datetime.timezone.utc).date()


def _families(sigs, ratio=0.90):
    """Group similar signatures WITHOUT merging them - the k8s triage merge
    idea, kept behind a human gate. Measured on this corpus, a blind merge
    at 0.90 joins genuinely different tests (mount + stop, --since +
    --until), so families are suggestions, never collapsed counts."""
    out, used = [], set()
    for i, a in enumerate(sigs):
        if a in used:
            continue
        fam = [a]
        for b in sigs[i + 1:]:
            if b in used:
                continue
            if abs(len(a) - len(b)) > max(len(a), len(b)) * 0.10:
                continue
            if difflib.SequenceMatcher(None, a, b).ratio() >= ratio:
                fam.append(b)
                used.add(b)
        if len(fam) > 1:
            used.update(fam)
            out.append(fam)
    return out


def _shown(sig, width):
    # truncate FIRST, then neutralise markdown - log content is untrusted
    s = (sig or "(none)")[:width]
    return s.replace("`", "'").replace("|", "\\|")


def full_report(with_issues=True, log=print):
    st = classify_all(load_state())
    repo = st["repo"]
    g = _groups(st)
    runs = st["runs"]
    if not runs:
        log("no state yet - run scan first")
        return None
    rerun = sum(1 for r in runs.values() if r["attempts"] > 1)
    days = sorted(r["created"] for r in runs.values())

    issues = matcher.fetch_issues(repo) if with_issues else []
    sig_counts = {sig: len(v) for sig, v in g.items() if sig}
    candidates = {r["sig"]: r for r in matcher.match(sig_counts, issues)} if issues else {}

    L = []
    L.append(f"# known flakes - {repo}")
    L.append("")
    sigged = sum(len(v) for sig, v in g.items() if sig)
    by_oracle = corroborate.summary(st)
    n_rerun = by_oracle.get(corroborate.RERUN, 0)
    n_corr = by_oracle.get(corroborate.CORROBORATED, 0)
    L.append(f"Generated {_today()}. "
             f"{len(runs)} completed runs ({days[0]} to {days[-1]}), {rerun} re-run by hand, "
             f"{len(st['flakes'])} flakes - {sigged} of them in "
             f"{len([s for s in g if s])} signatures, the rest with no marker or no log.")
    L.append("")
    L.append("The two oracles are counted separately on purpose, because the evidence behind "
             "them is not equally strong:")
    L.append("")
    L.append(f"- **{n_rerun} rerun-confirmed** - failed on one attempt and passed on a later "
             "attempt of the same run, so the commit never changed and there is a passing "
             "twin of that exact job to diff against.")
    L.append(f"- **{n_corr} corroborated** - a run nobody re-ran, whose failure signature was "
             "already proven flaky by a maintainer's own re-run elsewhere. There is no passing "
             "twin here, so this is the weaker of the two. Signatures that fail by design, such "
             "as the tests-included gate, are excluded from seeding it.")
    L.append("")
    L.append("Issue matches below are candidates, "
             "not verdicts - in the study this tool grew out of, 6 of 16 name-based matches "
             "moved once the logs were opened (docs/verification.md). Anything marked "
             "needs-check requires a human before it is used.")
    buckets = collections.defaultdict(list)
    for sig, v in g.items():
        buckets[v[0].get("bucket", "unknown")].append((sig, v))

    for bucket, title in [
        ("test", "test failures"), ("designed", "designed failures - not real flakes"),
        ("infra", "infrastructure"), ("unknown", "unmatched - open these by hand"),
        ("no-log", "no retrievable log"),
    ]:
        rows = sorted(buckets.get(bucket, []), key=lambda kv: -len(kv[1]))
        if not rows:
            continue
        real_sigs = len([sig for sig, _ in rows if sig])
        L.append("")
        head = f"## {title} ({sum(len(v) for _, v in rows)} flakes"
        head += f", {real_sigs} signatures)" if real_sigs else ")"
        L.append(head)
        L.append("")
        L.append("| n | signature | window | issue candidate |")
        L.append("|---|---|---|---|")
        for sig, v in rows:
            dates = sorted(x["date"] for x in v)
            win = f"{dates[0]} to {dates[-1]}" if dates[0] != dates[-1] else dates[0]
            cand = candidates.get(sig)
            c = ""
            if cand:
                flag = " needs-check" if cand["needs_human"] else ""
                c = f"#{cand['issue']}{flag}"
            L.append(f"| {len(v)} | `{_shown(sig, 90)}` | {win} | {c} |")
        model_rows = [(sig, v) for sig, v in rows
                      if sig and any(x.get("model") for x in v)]
        if model_rows:
            L.append("")
            L.append("model-suggested causes (unverified - a person confirms before "
                     "these are used anywhere):")
            for sig, v in model_rows[:10]:
                m = next(x["model"] for x in v if x.get("model"))
                L.append(f"- `{_shown(sig, 70)}` -> {m['cause']} ({m['confidence']})")
        fams = _families([sig for sig, _ in rows if sig])
        if fams:
            L.append("")
            L.append("possible families - similar signatures that MAY share one cause. "
                     "Kept separate above on purpose: similar names can be different "
                     "failures, so merging is a human call.")
            for fam in fams:
                total = sum(len(g[x]) for x in fam)
                L.append(f"- {total} flakes across {len(fam)}: " +
                         "; ".join(f"`{_shown(x, 60)}`" for x in fam[:4]) +
                         (" ..." if len(fam) > 4 else ""))
        # occurrence links for the top signature of each bucket
        if rows and rows[0][0]:
            L.append("")
            L.append(f"top signature occurrences:")
            for f in rows[0][1][:4]:
                L.append(f"- {_link(repo, f)}")

    os.makedirs(REPORTS, exist_ok=True)
    out = os.path.join(REPORTS, "known-flakes.md")
    open(out, "w").write("\n".join(L) + "\n")
    log(f"wrote {out}")
    return out


def weekly(log=print):
    st = classify_all(load_state())
    repo = st["repo"]
    cutoff = (_today() - datetime.timedelta(days=7)).isoformat()
    recent = [f for f in st["flakes"] if f["date"] >= cutoff]
    g = collections.defaultdict(list)
    for f in recent:
        g[f.get("sig")].append(f)

    L = [f"# flake report, week ending {_today()}", ""]
    if not recent:
        L.append("No confirmed flakes in the window.")
    else:
        L.append(f"{len(recent)} confirmed flakes in {len(g)} signatures this week.")
        L.append("")
        for sig, v in sorted(g.items(), key=lambda kv: -len(kv[1])):
            shown = _shown(sig, 100) if sig else "(no log / no marker)"
            L.append(f"## {len(v)}x  `{shown}`")
            L.append(f"jobs: {', '.join(sorted({x['job'].split(' / ')[0] for x in v}))}")
            for f in v[:3]:
                L.append(f"- {_link(repo, f)}")
            L.append("")
    os.makedirs(REPORTS, exist_ok=True)
    out = os.path.join(REPORTS, "weekly.md")
    open(out, "w").write("\n".join(L) + "\n")
    log(f"wrote {out}")
    return out
