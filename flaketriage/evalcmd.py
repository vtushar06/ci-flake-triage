"""Measure the model against hand labels. One command, per-class breakdown.

data/labels.json holds blind hand labels: signature -> cause, written by a
person from the evidence before seeing any model output. The number this
prints is the only honest answer to "is a small local model good enough" -
and if a prompt tweak helps or hurts, this is how a maintainer finds out.
"""
import collections
import json
import os

from . import model
from .analyze import build_prompt, causes
from .ingest import STATE, load_state

LABELS = os.path.join(os.path.dirname(STATE), "labels.json")


def run(log=print):
    if not os.path.exists(LABELS):
        log("no data/labels.json yet - label some signatures first")
        return None
    labels = json.load(open(LABELS))["labels"]
    st = load_state()
    by_sig = {}
    for f in st["flakes"]:
        if f.get("sig") and f.get("context") and f["sig"] not in by_sig:
            by_sig[f["sig"]] = f
    cs = causes()
    total = agree = 0
    pairs = collections.Counter()
    for sig, want in labels.items():
        f = by_sig.get(sig)
        if not f:
            continue
        text = model.chat(build_prompt(f["context"]))
        got = model.parse_verdict(text or "", cs)["cause"]
        total += 1
        agree += got == want
        pairs[(want, got)] += 1
        log(f"  {'ok ' if got == want else 'MISS'} want={want:16s} got={got:16s} {sig[:56]}")
    if total:
        log(f"\n{model.MODEL}: {agree}/{total} agree ({100*agree//total}%)")
        misses = [(w, g, n) for (w, g), n in pairs.items() if w != g]
        for w, g, n in sorted(misses, key=lambda x: -x[2]):
            log(f"  confused {w} -> {g} x{n}")
    return agree, total
