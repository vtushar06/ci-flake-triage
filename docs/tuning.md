# tuning - prompts, causes, and how to know a tweak helped

Everything a maintainer would tune lives outside the code:

- `prompts/classify.txt` - the classification prompt. `{causes}` and `{evidence}` are filled in
  at run time.
- `config/causes.json` - the label set with one line of meaning each. Add a cause here and it is
  immediately allowed; the model's answers are validated against this list and anything outside
  it becomes an explicit unknown.
- `data/labels.json` - blind hand labels, signature to cause. Written from the evidence before
  seeing any model output, so the eval means something.

The loop:

    edit prompts/classify.txt or config/causes.json
    python3 -m flaketriage eval

eval prints agreement against the hand labels, per-miss, with the confusion pairs. If the number
went up, the tweak helped. If you did not run eval, you do not know.

Two rules that are load-bearing:

- the model only ever sees a pre-extracted block or an attempt diff, never a raw log. That is
  what keeps a 3B local model workable and the cost bounded.
- the model's verdict lands in its own field and never overrides a rule bucket. Reports label it
  unverified. A person confirms before it is used anywhere.
