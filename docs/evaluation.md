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
