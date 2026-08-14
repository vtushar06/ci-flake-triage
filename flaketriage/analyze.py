"""Model verdicts over pre-extracted evidence. Optional, additive, gated.

The model never sees a raw log: it gets the context block from extract, or
the attempt diff when one is available (stronger evidence - lines unique to
the failing run). Its verdict lands in flake["model"], a separate field
that never overrides the rule bucket, and reports label it unverified.
"""
import json
import os

from . import model
from .ingest import STATE, load_state, save_state

CAUSES = os.path.join(os.path.dirname(STATE), "..", "config", "causes.json")
PROMPT = os.path.join(os.path.dirname(STATE), "..", "prompts", "classify.txt")


def causes():
    return json.load(open(CAUSES))["causes"]


def build_prompt(evidence):
    c = causes()
    listing = "\n".join(f"- {k}: {v}" for k, v in c.items())
    tpl = open(PROMPT).read()
    return tpl.replace("{causes}", listing).replace("{evidence}", evidence)


def analyze(limit=None, min_count=1, log=print):
    st = load_state()
    done = 0
    for f in st["flakes"]:
        if "model" in f or not f.get("context"):
            continue
        if limit and done >= limit:
            break
        text = model.chat(build_prompt(f["context"]))
        f["model"] = model.parse_verdict(text or "", causes())
        f["model"]["model"] = model.MODEL
        done += 1
        if done % 10 == 0:
            save_state(st)
            log(f"  {done} analyzed")
    save_state(st)
    log(f"done: {done} flakes analyzed with {model.MODEL}")
    return st
