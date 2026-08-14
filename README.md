# ci-flake-triage

A pipeline that finds confirmed flakes in a GitHub Actions workflow, classifies them, matches
them against the repo's open flake issues, and writes the report a reviewer can actually use.
It needs no change to the CI it watches - it reads only what the GitHub API already stores.

I built and ran this against podman's CI, over the full history of that project's `ci` workflow
since it moved off Cirrus - around 1300 completed runs at the time of writing, roughly 28% of them
re-run by hand, 550 confirmed flakes. The daily workflow keeps the exact current numbers in the
header of `reports/known-flakes.md`.

One thing worth knowing: the Actions runs listing stops at about 1000 results per query, so one
pass cannot see a longer history. `scan --created A..B` windows past the cap, and state is keyed
by run id so overlapping windows never double-count.

## the idea

Maintainers re-run jobs they believe failed for no real reason. That judgement is already in the
API: a job that failed on one attempt and passed on a later attempt of the same run cannot have
been the code, because the commit never changed. Walk the rerun history and you get a corpus of
confirmed flakes with zero instrumentation.

```
scan      incremental walk of completed runs, diff attempts, keep failed-then-passed jobs
extract   fetch each failing job's log, take the failure line via framework markers only
classify  rule buckets: test / designed / infra / no-log / unknown
match     candidate links to open flake-labelled issues, with the basis stated
report    known-flakes.md (everything) and weekly.md (last 7 days)
```

## run it

```
python3 -m flaketriage scan podman-container-tools/podman ci.yml
python3 -m flaketriage extract
python3 -m flaketriage report
python3 -m flaketriage weekly
python3 -m flaketriage propose            # draft issue comments - never posts
python3 -m flaketriage journal <job-id>   # fetch the job's systemd journal artifact
```

Needs python3 and a logged-in `gh`, nothing else. Read-only against GitHub - there is no code
path in this package that can post. State lives in `data/corpus.json` and scanning is
incremental, so after the first pass a daily run only touches new runs.

It runs itself: `.github/workflows/triage.yml` does the scan daily, runs the tests first, and
commits the refreshed corpus and reports back to the repo, so `reports/` on the default branch is
always current.

Tests: `python3 -m unittest discover tests`. The fixtures are real log shapes, including the
negative-test trap that once produced a confident wrong answer.

`journal` exists because the job log can point the wrong way (see below) - it turns the
five-API-call artifact dance into one command. A re-run leaves two same-named journal artifacts
on a run; the tool takes the failing attempt's, because the passing re-run's journal is a healthy
journal and silently answers the wrong question. That exact mistake happened while building this
and is now pinned by the disambiguation logic.

`propose` renders what the tool would comment on matched issues into
`reports/proposed-comments.md` and stops. A person reads them, checks anything marked
needs-check, and posts what survives. That gate is a design decision, not a missing feature - on
this data, 6 of 16 automated matches were wrong.

## the three rules that came from being wrong

Everything opinionated in this pipeline exists because the naive version produced a wrong answer
on real data first.

**Framework markers only, never a generic error grep.** Negative tests print expected errors
constantly. A greedy `Error:` pattern once produced a confident top flake out of a test literally
named "bad machine name".

**Issue matches are candidates, not verdicts.** Of 16 name-based matches against podman's open
flake issues, opening the actual logs moved six - in both directions. The matcher states its
basis (error string found verbatim in the issue body, or name similarity only) and flags
everything in the second class as needs-check.

**The job log can point the wrong way.** The most frequent signature in the corpus got a wrong
first diagnosis from its job log; the run's journal artifact showed the event the test waits for
firing 19-60 ms before the test starts listening. Classification here stops at what the log can
actually support, and the report says which results need a human with the artifact.

## what the model layer would be

Deliberately not built yet. The right shape, learned from the data above: deterministic
extraction does all the heavy lifting, and a small local model only ever classifies a
pre-extracted block of ~20 lines into a fixed set of causes, with its answer kept in a separate
field that never overrides a rule. Cheap enough to run locally, controllable, and checkable.

## files

- `flaketriage/` - the package, stdlib only
- `data/corpus.json` - full scan state, every confirmed flake with job, date and signature; buckets are derived at report time
- `reports/known-flakes.md` - generated: every signature bucketed, with issue candidates
- `reports/weekly.md` - generated: the last seven days
- `reports/proposed-comments.md` - generated: the drafts a human reviews before anything is posted
- `docs/verification.md` - the hand-verified triage of all 42 open flake issues
- `docs/healthcheck-deep-dive.md` - the worked example behind the journal rule, including the
  corrected diagnosis
