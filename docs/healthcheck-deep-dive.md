# `podman healthcheck` — podman's most frequent flake

> **CORRECTED 2026-08-05, and the correction matters more than the original.** Everything below
> about `FailingStreak` stopping at 2 is **wrong**. a maintainer said so on
> [#29353](https://github.com/podman-container-tools/podman/issues/29353#issuecomment-5169123492)
> on 2026-08-03 — *"the log appears before our since timestamp so we miss it"* — and the journal
> artifacts prove him right.
>
> The streak reaches 3 and the container does go unhealthy. Verified on two jobs:
>
> | job | container | unhealthy event | test `--since` | gap |
> |---|---|---|---|---|
> | 88658986341 | `c-h-t212-8z85pryk` | `14:29:20.897162043` streak=3 | `14:29:20,916284157` | **19.12 ms late** |
> | 89032377003 | `c-h-t212-cboduw61` | `19:56:46.344191789` streak=3 | `19:56:46,404004262` | **59.81 ms late** |
>
> The full ladder from `journal-sys-local-root-fedora-prior.log` for the first one is
> healthy/0, healthy/0, healthy/1, healthy/2, **unhealthy/3** — it never stalls.
>
> So the real defect is a race: `_check_health` captures its `--since` *after* the unhealthy event
> has already been emitted, and then polls a window that can never contain it. Raising the timeout
> (as [#29374](https://github.com/podman-container-tools/podman/pull/29374) proposes) cannot help,
> which is the one conclusion below that survives — for a different reason than the one given.
>
> **Why the original was wrong:** it read `FailingStreak:2` out of a `podman inspect` snapshot taken
> mid-run and treated a point-in-time value as a terminal state, without ever opening the journal
> artifact that records the events. The job logs alone cannot show this; the artifact can.
> Posted as [issuecomment-5216331863](https://github.com/podman-container-tools/podman/issues/29353#issuecomment-5216331863).

## Original write-up, kept for the record — the diagnosis below is superseded

**28 hits** in 1000 CI runs (2026-06-04 → 2026-07-30), across four distro/privilege combinations.
The single largest genuine flake signature in the corpus. It has no open issue.

Test: `test/system/220-healthcheck.bats`, `@test "podman healthcheck"`, tagged `ci:parallel`.
Symptom, in 4 of 5 sampled jobs, identical wording:

```
#| FAIL: Four or more failures - timed out waiting for 'unhealthy' in podman events
```

## What everyone will assume, and why it is wrong

The message says "timed out", the helper has a counter that starts at 5, and the container is
configured `--health-interval 1s --health-retries 3`. So 3 failures ought to take ~3s and 5s looks
tight. The obvious patch is to raise the timeout.

**Measured, that patch would change nothing.** The loop in `_check_health` decrements its counter
once per iteration, but each iteration also runs `podman events`, so an iteration costs ~1.3s, not
1s. Actual time the test waited before giving up:

| job | events polls | time waited | result |
|---|---|---|---|
| 88421964442 | 11 | **13.77 s** | died |
| 88677981054 | 11 | **11.98 s** | died |
| 89032377003 | 8 | 10.51 s | died |
| 88658986341 | 8 | 8.29 s | died |
| 88684738266 | 3 | 1.97 s | passed |

The test waits 8 to 14 seconds for something that should take 3. Raising the number would just
make CI slower for the same failure.

## What actually happens

Every failing job stops in exactly the same place:

```json
{"Status":"healthy","FailingStreak":2,"Log":[{...ExitCode:0},{...0},{...1},{...1}]}
```

Two failures recorded, then nothing. `--health-retries 3`, so the container never turns
`unhealthy`, so the event the test waits for is never emitted.

Time spent stuck on `FailingStreak=2`, measured from that inspect to the last events poll:

| job | stuck for |
|---|---|
| 88421964442 | ~10.3 s |
| 88677981054 | 8.57 s |
| 89032377003 | 10.63 s |

At the measured interval that window should have produced **eight or nine more checks**. It
produced none.

And the timer is not gone. Job 88421964442 prints `systemctl list-units` right in the middle of
the stall:

```
…-4d5f2e5e0f0173c3.service  loaded  active  running
…-4d5f2e5e0f0173c3.timer    loaded  active  running
```

So: timer active, interval nominally 1s, and no healthcheck runs for ten seconds.

## Ruled out, with the evidence

| hypothesis | verdict |
|---|---|
| test timeout too short | **no** — it waits 8-14 s, see table above |
| systemd timer jitter | **no** — 16 intervals measured across 5 jobs: median **1.10 s**, p90 1.31 s, only one outlier at 2.49 s |
| systemd `AccuracySec` defaulting to 1 min | **no** — `libpod/healthcheck_linux.go:45` already passes `--timer-property=AccuracySec=1s` |
| `--health-on-failure=kill` firing early | **no** — `processHealthCheckStatus` returns immediately unless status is `unhealthy` (`libpod/healthcheck.go:200`) |
| `FailingStreak` accounting | **correct** — `healthcheck.go:397-401` increments then compares `>= Retries` |
| start-period suppressing the increment | **not confirmed** — `healthcheck.go:395` only counts when `!inStartPeriod`, and the test does set `--health-startup-cmd`; the streak did reach 2, so it was not suppressed then. Worth checking whether it can flip back |

## Where this stops

The remaining question is why `podman healthcheck run` produces no new log entry for ~10 seconds
while its systemd timer is active. That needs a Linux host with podman to reproduce; this machine
has only the macOS client, so it is not settled here.

The timer is created with `--on-unit-inactive=<interval>` (`healthcheck_linux.go:45`), meaning it
re-arms relative to the *service* going inactive rather than on a fixed schedule. A transient
service that exits non-zero — which is exactly what a failing healthcheck does — is the obvious
thing to look at next.

## Why this is worth reporting even unfinished

If a categoriser, or a person, reads "timed out waiting for 'unhealthy'" and stops there, the fix
is a bigger timeout. That fix is measurably useless and would slow CI. The value here is the
disproof, not a patch.

This is also the concrete example for the proposal: automated triage gets to *"healthcheck, 28
times, timeout message"*. Everything above needed somebody to open five logs and measure. That gap
is the argument for a human confirmation step.
