"""Minimal LLM backends.  Tests and toy runs use ``MockBackend``; real runs use any OpenAI-compatible
endpoint (OpenAI, vLLM, Ollama, DeepSeek, ...) and should wrap it in ``CachedBackend`` so that every raw
response is stored (provenance + exact re-analysis without re-querying).

Never point an attack run at a third-party *agent product*; point it at a model API you are allowed
to use, with the victim system running locally (see skills/ethics-disclosure).
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.request
from typing import Callable, Protocol

Messages = list[dict]


class Backend(Protocol):
    name: str

    def chat(self, messages: Messages, **kw) -> str: ...


class MockBackend:
    """Deterministic backend: ``fn(messages) -> str``.  ``name`` is recorded in results as the model id."""

    def __init__(self, fn: Callable[[Messages], str], name: str = "mock"):
        self.fn, self.name, self.calls = fn, name, 0

    def chat(self, messages: Messages, **kw) -> str:
        self.calls += 1
        return self.fn(messages)


class OpenAICompatible:
    """POST {base_url}/chat/completions.  The API key is read from the environment, never stored."""

    def __init__(self, base_url: str, model: str, api_key_env: str = "OPENAI_API_KEY", temperature: float = 0.0,
                 max_tokens: int | None = None, timeout: float = 120.0, retries: int = 3):
        self.base_url, self.model, self.api_key_env = base_url.rstrip("/"), model, api_key_env
        self.temperature, self.max_tokens, self.timeout, self.retries = temperature, max_tokens, timeout, retries
        self.name = model

    def chat(self, messages: Messages, **kw) -> str:
        body = {"model": self.model, "messages": messages, "temperature": kw.get("temperature", self.temperature)}
        if self.max_tokens or kw.get("max_tokens"):
            body["max_tokens"] = kw.get("max_tokens", self.max_tokens)
        if "seed" in kw:
            body["seed"] = kw["seed"]
        headers = {"Content-Type": "application/json"}
        key = os.environ.get(self.api_key_env, "")
        if key:
            headers["Authorization"] = f"Bearer {key}"
        req = urllib.request.Request(f"{self.base_url}/chat/completions", data=json.dumps(body).encode(), headers=headers)
        last = None
        for i in range(self.retries):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    data = json.loads(r.read())
                return data["choices"][0]["message"].get("content") or ""
            except Exception as e:  # noqa: BLE001 -- network errors vary by platform
                last = e
                time.sleep(2 ** i)
        raise RuntimeError(f"{self.model}: request failed after {self.retries} tries: {last}")


class CachedBackend:
    """Append-only jsonl cache keyed by sha256(model, messages, kwargs).  Doubles as the raw-response log."""

    def __init__(self, inner: Backend, path: str):
        self.inner, self.path, self.name = inner, path, inner.name
        self.hits = self.misses = 0
        self._cache: dict[str, str] = {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        rec = json.loads(line)
                        self._cache[rec["key"]] = rec["response"]

    def _key(self, messages: Messages, kw: dict) -> str:
        blob = json.dumps({"model": self.inner.name, "messages": messages, "kw": kw}, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def chat(self, messages: Messages, **kw) -> str:
        k = self._key(messages, kw)
        if k in self._cache:
            self.hits += 1
            return self._cache[k]
        self.misses += 1
        out = self.inner.chat(messages, **kw)
        self._cache[k] = out
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"key": k, "model": self.inner.name, "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                 "messages": messages, "kw": kw, "response": out}, ensure_ascii=False) + "\n")
        return out


def from_config(cfg: dict) -> Backend:
    """``{"type": "openai", "base_url": ..., "model": ..., "api_key_env": ..., "cache": "results/x/cache.jsonl"}``
    or ``{"type": "mock-rumor", ...}`` (the toy rule-based agents used by the case study and tests)."""
    t = cfg.get("type", "openai")
    if t == "openai":
        b: Backend = OpenAICompatible(cfg["base_url"], cfg["model"], cfg.get("api_key_env", "OPENAI_API_KEY"),
                                      cfg.get("temperature", 0.0), cfg.get("max_tokens"))
    elif t == "mock-rumor":
        from .toy import rumor_mock
        b = rumor_mock(cfg.get("gullibility", 0.5), cfg.get("seed", 0), cfg.get("model", "mock-rumor"))
    else:
        raise ValueError(f"unknown backend type {t!r}")
    return CachedBackend(b, cfg["cache"]) if cfg.get("cache") else b
