# evaluation - what is measured and what is not

The labelled set (`data/labels.json`) is small and honest: signatures labelled by hand from the
evidence, blind, before any model output was seen. Seeded from the deep dives whose causes were
verified the hard way (healthcheck = test-side race in the --since capture, prune and rmi =
concurrent teardown races, the make gate = designed failure). Growing it is a human task and the
protocol matters more than the count: label from the log and journal evidence, then compare.

What eval reports: agreement, per-miss detail, confusion pairs. What it deliberately does not
report: anything about signatures with no context block, and anything the model was never asked.

Known limits, stated rather than hidden:

- the labelled set is written by the same people who wrote the rules; the guard is the blind
  protocol and the set being committed here for anyone to re-check.
- confidence is self-reported by the model and treated as a display hint, not a probability.
- an attempt diff is stronger evidence than a context block, but it needs both logs to still be
  retrievable; the eval states which evidence each row used.

## what the literature says to expect

Calibration, so nobody is surprised by the first number:

- FlakyCat (AST 2023), a trained specialist on ~340 labelled flaky tests, tops out around
  weighted F1 0.70 on four causes - and its worst class is concurrency, exactly our hardest.
- zero-shot open 7B models given only test source code land near the floor (FlakeBench: macro F1
  under 15). That is why this pipeline never does zero-shot-over-source.
- LogEval: few-shot examples are the biggest lever for small models on log tasks (Qwen-7B 0.33
  zero-shot to 0.52 few-shot); and a 2026 severity benchmark got a 4B model to 95% only with
  retrieved similar labelled examples in the prompt - our labelled corpus can double as exactly
  that retrieval pool later.
- no published benchmark classifies flake causes from failing-vs-passing attempt diffs. Our
  input format has no prior number; the harness here is how one gets established.

The strongest external support for this design is Gultekin, Berndt, Bell, Bach and Baltes,
"How Far Are We from Detecting Flaky Tests? On the Limits of Code-Based Detection"
(arXiv 2607.09345, 2026). Two findings land directly on choices made here:

- they argue the field should ask whether **an observed failure is flaky** rather than whether a
  test *can* be flaky. That is exactly what the rerun-history oracle answers, and it is the
  reason this pipeline is built on observed reruns rather than on static analysis of test code.
- across 86 end-to-end CI failures, the test code revealed the cause in only 42%; **58% needed
  additional execution evidence**. That is the published form of what cost me a public
  correction on podman #29353, where the job log pointed the wrong way and the systemd journal
  artifact held the actual cause. It is why artifact fetching is part of ingestion rather than
  an afterthought.

Jonathan Bell also confirmed by email (2026-08-19) that mass reruns surface proportionally more
infrastructure defects - transient DNS failures were his example. Our corpus is human-triggered
rather than mass-rerun, so it is biased the other way, toward failures a maintainer thought were
worth acting on. That is a different population, not a smaller one, and worth stating whenever
these numbers are compared to rerun-harness studies.

Sizing target from the same literature: ~30 labelled items per cause before per-class numbers
mean anything. Until then the headline is the overall agreement plus coverage, nothing finer.
