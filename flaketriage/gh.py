"""Thin wrapper around the gh CLI. All GitHub access goes through here.

gh handles auth; this wrapper retries with backoff on rate limits and
transient errors. Read-only - nothing in this package writes to GitHub.

api() returns None ONLY for a hard 404/410 (the thing is gone). Auth
failures exit with gh's own message, and exhausted retries raise - a
caller must never mistake "the API was down" for "there were no jobs",
because recording a rerun as processed with zero flakes loses those
flakes forever.
"""
import json
import subprocess
import time


class ApiError(RuntimeError):
    pass


def api(path, tries=3):
    """GET a REST path, parsed. None only when the resource is gone."""
    err = ""
    for i in range(tries):
        r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
        if r.returncode == 0:
            return json.loads(r.stdout) if r.stdout.strip() else None
        err = r.stderr.strip()
        low = err.lower()
        if "404" in low or "410" in low or "gone" in low:
            return None
        if "401" in low or "bad credentials" in low or "gh auth login" in low:
            raise SystemExit(f"gh is not authenticated: {err.splitlines()[0] if err else 'run gh auth login'}")
        # rate limit or transient - back off and retry
        time.sleep(5 * (i + 1))
    raise ApiError(f"gh api {path} failed after {tries} tries: {err.splitlines()[0] if err else 'unknown error'}")


def api_text(path):
    """GET a path that returns plain text (job logs). None if the log is gone."""
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def api_bytes(path):
    """GET a path that returns binary data (artifact zips)."""
    r = subprocess.run(["gh", "api", path], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def paginate(path, key):
    """Yield items across all pages."""
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        d = api(f"{path}{sep}per_page=100&page={page}")
        items = (d or {}).get(key, [])
        if not items:
            return
        yield from items
        page += 1
