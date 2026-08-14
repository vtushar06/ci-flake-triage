"""Draft what the tool WOULD post, without posting anything.

There is deliberately no write path to GitHub anywhere in this package.
On this data, automated issue matching was wrong often enough (6 of 16
moved on log inspection) that publishing without a human gate would erode
the exact trust the tool exists to build. So this stage renders the
drafts into a file and stops. A person reads them, checks the flagged
ones, and posts what survives.
"""
import datetime
import os

from .classify import classify_all
from .ingest import STATE, load_state
from . import match as matcher
from .report import _groups, _link

REPORTS = os.path.join(os.path.dirname(STATE), "..", "reports")


def proposals(min_count=3, log=print):
    st = classify_all(load_state())
    repo = st["repo"]
    g = _groups(st)
    issues = matcher.fetch_issues(repo)
    sig_counts = {s: len(v) for s, v in g.items() if s}
    rows = matcher.match(sig_counts, issues)

    L = [f"# proposed issue comments - {datetime.date.today()}",
         "",
         "Drafts only. Nothing below has been posted and this tool has no code path",
         "that can post. Matches marked needs-check failed the verbatim-error test",
         "and must not be used without opening the logs first.",
         ""]
    n = 0
    for r in rows:
        if r["count"] < min_count:
            continue
        n += 1
        flakes = g[r["sig"]]
        dates = sorted(f["date"] for f in flakes)
        L.append(f"## draft {n}: issue #{r['issue']}" + ("  [needs-check]" if r["needs_human"] else ""))
        L.append(f"match basis: {r['basis']}")
        L.append("")
        L.append("```")
        L.append(f"this is still firing - {r['count']} times between {dates[0]} and {dates[-1]}:")
        L.append("")
        L.append(f"    {r['sig'][:120]}")
        L.append("")
        for f in flakes[:3]:
            L.append(_link(repo, f))
        L.append("```")
        L.append("")
    if n == 0:
        L.append(f"No matched signature reached {min_count} occurrences.")
    os.makedirs(REPORTS, exist_ok=True)
    out = os.path.join(REPORTS, "proposed-comments.md")
    open(out, "w").write("\n".join(L) + "\n")
    log(f"wrote {out} ({n} drafts)")
    return out
