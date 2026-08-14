# architecture

Written in the shape of podman's own design-doc template (contrib/design-docs/TEMPLATE.md), so it
can become a real design PR if the project ever wants one. Everything marked designed-not-built is
exactly that.

## Short Summary

A pipeline that turns GitHub Actions rerun history into a maintained flake list, a per-cause
classification, and human-gated reports - with no change to the CI it watches.

## Objective

Reviewers are told to check whether a failing test is a known flake, and no current list exists.
Maintainers re-run jobs by hand and the information in those re-runs evaporates. This tool keeps
it.

## Detailed Description

Stages, each a module, each runnable alone:

    scan     GitHub API: completed runs, run_attempt > 1, diff attempts.
             failed-then-passed on the same commit = confirmed flake.
    extract  failing job log -> failure line via framework markers only,
             plus a context block around it. no generic error grep.
    diff     the same run has a FAILING attempt log and a PASSING attempt
             log for the same job on the same commit. diff them. races,
             infra blips and network timeouts separate here, before any
             model sees anything.
    classify rules first (test/designed/infra/no-log/unknown), from config.
    analyze  (model, optional) a small model reads the pre-extracted block
             or the attempt diff - never a raw 1000-line log - and returns
             {cause, confidence, deciding_line}. stored in its own field,
             never overrides a rule.
    match    candidates against open flake-labelled issues, basis stated,
             name-only matches flagged needs-check.
    report   known-flakes.md, weekly.md, proposed-comments.md (drafts only,
             no code path can post).

Design decisions and the mistakes behind them:

- markers only, never a generic error grep - a greedy grep once invented a confident wrong top
  flake out of a negative test.
- the job log can point the wrong way - the top signature's first diagnosis was wrong until the
  systemd journal artifact was read. journal fetch is one command.
- issue matches are candidates - 6 of 16 name matches moved when logs were opened.
- similar signatures are suggested as families, never merged - a measured 0.90 merge joined
  genuinely different tests.
- prompts and cause buckets live in files (prompts/, config/), because maintainers must be able
  to tweak both without touching code, and an eval command must tell them whether the tweak
  helped.
- provider-agnostic model client, local default. the hosted free option evaluated for this
  (GitHub Models) was retired mid-build - HTTP 410, "retirement brownout" - which is the
  dependency-risk argument made real.

## Use cases

- a reviewer checks whether a red job is known: open reports/known-flakes.md, search the test.
- a maintainer wants the week's picture: reports/weekly.md, one screen.
- a debugger wants the truth about one flake: flaketriage journal <job-id>, then diff.
- triage wants issue updates: flaketriage propose, human reads, posts what survives.

## Prototype status

built and tested: scan, extract, classify, match, report, journal, families, daily workflow.
designed, not built: diff (next), analyze + eval (next), occurrence-ledger comments
(cockpit-style), Drain3 trial for marker-less unknowns.
