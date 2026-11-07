"""Validate an LLM (or rule-based) judge against human gold labels before trusting its ASR.

Typical use: label a stratified sample of 100-200 transcripts by hand, run the judge on the same
items, then ``agreement_report(gold, pred)``; target Cohen's kappa >= 0.7 and report the judge's
precision/recall for the positive ("attack succeeded") class next to every ASR it produced.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Hashable, Sequence


def confusion(gold: Sequence[Hashable], pred: Sequence[Hashable]) -> dict[tuple, int]:
    if len(gold) != len(pred):
        raise ValueError(f"gold and pred differ in length ({len(gold)} vs {len(pred)})")
    return dict(Counter(zip(gold, pred)))


def cohen_kappa(a: Sequence[Hashable], b: Sequence[Hashable]) -> float:
    """Cohen's kappa for two raters over the same items (any hashable labels)."""
    if len(a) != len(b):
        raise ValueError("raters must label the same items")
    n = len(a)
    if n == 0:
        raise ValueError("no items")
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


def agreement_report(gold: Sequence[Hashable], pred: Sequence[Hashable], positive: Hashable = True) -> dict:
    """Accuracy, kappa and judge precision/recall/F1 for the positive class, plus the confusion matrix."""
    cm = confusion(gold, pred)
    n = len(gold)
    tp = sum(v for (g, p), v in cm.items() if g == positive and p == positive)
    fp = sum(v for (g, p), v in cm.items() if g != positive and p == positive)
    fn = sum(v for (g, p), v in cm.items() if g == positive and p != positive)
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if tp and prec + rec else 0.0
    return {
        "n": n,
        "accuracy": sum(v for (g, p), v in cm.items() if g == p) / n if n else float("nan"),
        "kappa": cohen_kappa(gold, pred),
        "precision": prec, "recall": rec, "f1": f1,
        "confusion": {f"{g}->{p}": v for (g, p), v in sorted(cm.items(), key=str)},
    }


def fingerprint(prompt: str, model: str, temperature: float = 0.0, **extra) -> str:
    """Stable sha256 of the judge configuration; record it in EVIDENCE rows that use the judge."""
    blob = json.dumps({"prompt": prompt, "model": model, "temperature": float(temperature), **extra},
                      sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
