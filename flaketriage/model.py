"""OpenAI-compatible chat client, stdlib only.

Provider-agnostic on purpose: FLAKETRIAGE_MODEL_URL points at ollama
(http://localhost:11434/v1, the default), llama.cpp server, or any hosted
endpoint; FLAKETRIAGE_MODEL names the model; FLAKETRIAGE_MODEL_KEY is only
needed by hosted providers. The hosted free option evaluated while building
this (GitHub Models) was retired mid-build, which is why nothing here
depends on any one provider existing.
"""
import json
import os
import urllib.request

URL = os.environ.get("FLAKETRIAGE_MODEL_URL", "http://localhost:11434/v1")
MODEL = os.environ.get("FLAKETRIAGE_MODEL", "qwen2.5:3b")
KEY = os.environ.get("FLAKETRIAGE_MODEL_KEY", "")


def chat(prompt, timeout=120):
    """One prompt in, the text of the first choice out. Raises on transport
    errors; returns None only when the endpoint answered but with nothing."""
    req = urllib.request.Request(
        URL.rstrip("/") + "/chat/completions",
        data=json.dumps(
            {
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "response_format": {"type": "json_object"},
            }
        ).encode(),
        headers={"Content-Type": "application/json"}
        | ({"Authorization": f"Bearer {KEY}"} if KEY else {}),
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    choices = d.get("choices") or []
    return choices[0]["message"]["content"] if choices else None


def parse_verdict(text, causes):
    """The model's JSON, validated against the configured cause list.
    Anything malformed becomes an explicit unknown - never a crash, never
    a silently accepted invalid label."""
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        d = json.loads(text[start:end])
    except (ValueError, AttributeError):
        return {"cause": "unknown", "confidence": "low", "deciding_line": "", "note": "unparseable"}
    if d.get("cause") not in causes:
        return {"cause": "unknown", "confidence": "low", "deciding_line": "", "note": "invalid label"}
    d.setdefault("confidence", "low")
    d.setdefault("deciding_line", "")
    return {k: d[k] for k in ("cause", "confidence", "deciding_line")} | (
        {"note": d["note"]} if "note" in d else {}
    )


def verify_deciding_line(verdict, evidence):
    """The strongest anti-noise check available: the model must quote the
    line that decided it, and that line must actually be in the evidence.
    A hallucinated quote downgrades the verdict to unknown."""
    line = (verdict.get("deciding_line") or "").strip()
    if verdict["cause"] != "unknown" and line and line not in (evidence or ""):
        return {"cause": "unknown", "confidence": "low", "deciding_line": "",
                "note": "deciding_line not found in evidence"}
    return verdict
