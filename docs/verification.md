# hand verification - the layer the pipeline deliberately does not automate

The pipeline gets you to "this signature, N times, these jobs". This file is what the human layer
found when every automated answer was checked against the actual logs, and it is why the matcher
only ever emits candidates. Sections below are from the 1000-run pass; the pipeline's
`reports/known-flakes.md` regenerates the mechanical parts from the full history on every run.

# podman open flake issues — which are still happening

`REVIEWING.md` asks reviewers to "check to see if those tests failed due to known flakes". No such
list has existed since the Cirrus migration. This is that list, built from CI data rather than
memory.

**Method.** 1000 completed `ci` workflow runs, **2026-06-04 to 2026-07-30**. The `ci` workflow was
added on **2026-05-25** and has **1083 completed runs** in total, so this covers essentially the
whole of CI since the migration. 277 of them (27.7%)
were re-run by hand — every one of those is a maintainer saying they thought the failure was not
real. A job that failed on an early attempt and passed on the final attempt of the *same* run, with
the commit unchanged, is a confirmed flake: **417 of them**, collapsing into **145 signatures**.

Each of the 42 open `flakes` issues was then matched against those signatures, and every proposed
match was checked by opening the actual job log and looking for the issue's own error string. That
step changed the answer often enough that it is the main finding in itself — see *What the checking
changed* at the bottom.

(For rough scale only: one published measurement of GitHub Actions re-run rates across Java
projects sits around 3%. Different ecosystem, different definition, so read it as context, not a
comparison.)

---

## Still happening — same test, same error

| issue | hits | window | evidence |
|---|---|---|---|
| [#28868](https://github.com/podman-container-tools/podman/issues/28868) prune --build | 12 | 06-04 → 07-21 | but **four** distinct failure modes, see below |
| [#24598](https://github.com/podman-container-tools/podman/issues/24598) commit: layer not known | 4 | 06-11 → 07-27 | `layer not known` in 2 of 3 sampled logs, inside the `quadlet - image tag` bats test |
| [#28873](https://github.com/podman-container-tools/podman/issues/28873) windows machine rename | 3 | 06-05 → 07-08 | the issue's own job is in the corpus; `Access is denied` on the `.tmp-…json` rename, jid 79772780772 |
| [#17957](https://github.com/podman-container-tools/podman/issues/17957) system reset: unlinkat | 2 | 06-10 → 06-17 | `unlinkat …/clitmp/events: directory not empty` verbatim, jid 82012715157 |
| [#23479](https://github.com/podman-container-tools/podman/issues/23479) misc parallel flakes | 2 | 06-19 → 07-26 | `logs --since -f` on journald emits nothing before the 3s TERM; the umbrella body lists this test |
| [#24800](https://github.com/podman-container-tools/podman/issues/24800) images concurrent removal | 2 | 06-24 → 07-08 | `retrieving label for image …: you may need to remove the image` verbatim in both |
| [#19048](https://github.com/podman-container-tools/podman/issues/19048) run -P TOCTOU | 2 | 06-04 → 06-11 | `cannot bind tcp port :41545: address already in use`; wording changed since 2023, race identical |
| [#23682](https://github.com/podman-container-tools/podman/issues/23682) logs --until --follow | 1 | 06-15 | `podman logs --until: exited too late!` verbatim, jid 81482563198 |
| [#23871](https://github.com/podman-container-tools/podman/issues/23871) healthcheck races | 1 | 06-29 | `Container went from starting to healthy`, `700-play.bats:934`, `ci:parallel` |
| [#24622](https://github.com/podman-container-tools/podman/issues/24622) kube down aardvark | 1 | 06-29 | aardvark / unmarshalling error present, jid 84249044760 |
| [#20485](https://github.com/podman-container-tools/podman/issues/20485) build secrets ENOENT | 1 | 06-24 | same failure, not just same test |
| [#22551](https://github.com/podman-container-tools/podman/issues/22551) machine uncategorized | 1 | 07-09 | **medium confidence** — fits by umbrella policy, not error string |

## Test unstable in the window; the recorded error was not observed

The test is demonstrably unstable, but the issue's error does not appear. Closing these would be
wrong; so would claiming they are still reproducing.

| issue | what the corpus actually shows |
|---|---|
| [#22843](https://github.com/podman-container-tools/podman/issues/22843) Windows socket identity | 3 hits of the gvproxy test, **0** with `failed to read identity`. Instead `connectex: actively refused`, `ssh error`, `EOF`. The issue's own hits were Cirrus-era hyperv-rootless; corpus hits are GHA wsl/applehv |
| [#21540](https://github.com/podman-container-tools/podman/issues/21540) manifest auth push | 1 hit, but a 90s hang in a `crypto/tls` read loop, not the `HTTP request to an HTTPS server` 400 |
| [#10710](https://github.com/podman-container-tools/podman/issues/10710) tty resize stty | 1 hit, but the socat-created test PTY disappearing, not the 2021 resize race |

## Rejected

| issue | why |
|---|---|
| [#23615](https://github.com/podman-container-tools/podman/issues/23615) logs k8s-file | Matched on `logs --since --follow` but the corpus hits are the **journald** driver; the issue is **k8s-file**, and its author writes *"I don't think it's the same as … #23479"* |

## Not seen in 1000 runs

Absence over 8 weeks is not proof of a fix. Each named test still exists in the tree — none of
these are "test deleted".

**Can't currently be observed** — the job or path is not in GitHub Actions CI:

- [#28300](https://github.com/podman-container-tools/podman/issues/28300) aarch64 machine slowness — the arm runner is **commented out**, not removed, at `.github/workflows/ci.yml:447`, with the note that CNCF may supply a bare-metal host. Parked, not fixed.
- [#17802](https://github.com/podman-container-tools/podman/issues/17802) quay 502 and [#17804](https://github.com/podman-container-tools/podman/issues/17804) quay V1 — `test/registries-cached.conf`, which `hack/ci/runner.sh:102` installs in CI, redirects `prefix="quay.io"` to `127.0.0.1:60333`. CI does not pull from real quay, so a quay outage can no longer produce these.

**Probably closable** — concrete evidence, the only one of 42 to survive an adversarial check:

- [#18484](https://github.com/podman-container-tools/podman/issues/18484) search wildcards — the test was rewritten. `test/e2e/search_test.go` now searches `registryAddress + "/*alpine*"` with `--tls-verify=false` against the local test registry; `registry.access.redhat.com` appears **zero** times in the file. The external registry that caused the flake is no longer touched.

**Rare, keep open** — test and platform both still live, it simply did not fire in this window:
#18856, #18793, #27455, #27264, #26547 (wsl is still in the matrix, `ci.yml:228`), #23454, #23385
(composefs still enabled on rawhide, `runner.sh:31`), #21741, #24223, #24220, #24010, #25855,
#24571, #24258, #21560, #20332, #18890, #17288, #17193, #16154, #15074, #10927.

Two worth a note: checkpoint tests **do** flake in this window under three other signatures, just
not the criu-version-detection one (#18856) or the incomplete-restore one (#24571). And #24220 is
about **podman-remote** logs; the three journald `events` hits in the corpus are all `sys local`,
so they are a relative, not a match.

---

## #28868 hides four failure modes, not one

All 12 instances read individually:

| what failed | n | error |
|---|---|---|
| prune exits 125 | 3 | `Error: container not known` |
| prune exits 125 | 2 | `Error: identifier is not a container` |
| prune exits 125 | 2 | `Error: replacing mount point …/merged: directory not empty` |
| **prune never ran** | 5 | assert at `prune_test.go:651` — `ps -aq --external` returned 1–2 containers, expected 3 |

The first two are `stypes.ErrContainerUnknown` and `stypes.ErrNotAContainer`
(`vendor/go.podman.io/storage/types/errors.go:9` and `:41`).

The 5 in the last row are a **different bug from the one the issue records**: the terminated
build's external containers have not appeared yet, so the setup assertion fails before
`system prune --build` is ever invoked. That is a setup race, not a prune race, and nothing
currently open tracks it.

## What the checking changed

Of 16 proposed matches, opening the logs moved **six** of them, and in both directions:

- **#24598** and **#24622** looked like obvious false positives — the corpus signatures
  (`quadlet - image tag`, `kube play healthcheck …`) have nothing to do with the issue titles.
  Both were right: the issues' own pasted logs show those same bats tests.
- **#23615** looked obviously right and was wrong — journald vs k8s-file.
- **#22843**, **#21540**, **#10710** all flake in the corpus but with a different error than
  recorded.
- **#28868** is right, but under an error string the issue never mentions.

**A matching test name is not a matching failure.** An automated categoriser that stops at the test
name would have published a backlog report with at least four wrong entries. Nothing here should be
posted without a human opening one log first.

The same held for the "is it dead" question: three issues were first judged not-plausible, and an
adversarial second pass refuted two of them (#28300, #24571). Only #18484 survived.

## The 42 are not the whole picture

Two things fall outside any open issue, and both matter more than the backlog itself.

**The most frequent flake in the window had no issue at all.** `podman healthcheck`, 28 hits, more
than any of the 42. Filed as
[#29353](https://github.com/podman-container-tools/podman/issues/29353) on 2026-07-31, and corrected
on 2026-08-05 after maintainer feedback: the journal artifacts show the unhealthy event landing
19-60 ms before the test captures its `--since` timestamp, so the poll window can never contain the
event it is waiting for. A longer timeout does not change that. The correction only came from
opening the journal artifacts - the job log alone points the wrong way.

**A failing job does not always leave anything to categorise.** In that same run, five jobs finished
`conclusion: failure` with step `Run test on lima` still at conclusion `None` and logs returning
`BlobNotFound`, each after 27-28 minutes against a 30 minute job budget (`ci.yml:380` into
`lima.yml:42`). No failure marker, no test report, nothing for a categoriser to read.

How common that is depends on how you count: the strict shape (step stuck at `None`, 27-28 min)
appeared once across 80 runs, but a looser sweep over a later window found 43 log-less failed jobs
across four runs, most on superseded attempts where GitHub may simply no longer serve the log. The
honest position is that the class exists, its size is unsettled, and a categoriser must not crash
or invent a signature when a job has no output.
