"""Match flake signatures against the repo's open flake-labelled issues.

Output is CANDIDATES with a stated basis, never verdicts. On the podman
data, 6 of 16 name-based matches moved once the actual logs were opened -
in both directions. A tool that publishes name matches as facts would have
shipped a report with wrong entries, so this one refuses to.
"""
import re

from . import gh


def _tokens(s):
    return set(re.findall(r"[a-z0-9_]{3,}", (s or "").lower())) - {
        "podman", "test", "tests", "the", "and", "with", "for", "not",
    }


def fetch_issues(repo, label="flakes"):
    # the issues endpoint returns a bare list, so page manually
    out = []
    page = 1
    while True:
        d = gh.api(f"repos/{repo}/issues?state=open&labels={label}&per_page=100&page={page}")
        if not d:
            break
        for i in d:
            if "pull_request" not in i:
                out.append({"number": i["number"], "title": i["title"], "body": i.get("body") or ""})
        if len(d) < 100:
            break
        page += 1
    return out


def match(signatures, issues):
    """signatures: {sig: count}. Returns candidate rows sorted by score."""
    rows = []
    for sig, count in signatures.items():
        if not sig:
            continue
        stok = _tokens(sig)
        best, best_score, basis = None, 0.0, ""
        for iss in issues:
            ttok = _tokens(iss["title"])
            btok = _tokens(iss["body"])
            # symmetric overlap - normalising by the issue title alone let a
            # one-word generic title score 1.0 and beat the real match
            title_overlap = len(stok & ttok) / max(len(stok | ttok), 1)
            # an error string appearing verbatim in the issue body outranks
            # any amount of name similarity
            err = sig.split(":", 1)[-1].strip()
            verbatim = bool(err) and len(err) > 20 and err.lower() in iss["body"].lower()
            score = (2.0 if verbatim else 0.0) + title_overlap + 0.3 * (len(stok & btok) / max(len(stok), 1))
            if score > best_score:
                best, best_score = iss, score
                basis = "error string appears in issue body" if verbatim else "name similarity only"
        # 0.3 is set from the hand-verified triage: a confirmed-true name
        # match (quadlet image tag) scores 0.30 under this metric. Recall
        # matters more than precision here - every name-based row is flagged
        # needs-check and a human filters them.
        if best and best_score >= 0.3:
            rows.append(
                {
                    "sig": sig,
                    "count": count,
                    "issue": best["number"],
                    "title": best["title"][:70],
                    "basis": basis,
                    "needs_human": basis != "error string appears in issue body",
                }
            )
    return sorted(rows, key=lambda r: -r["count"])
