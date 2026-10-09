"""Polite HTTP access to Wikimedia APIs: descriptive User-Agent, rate limit, backoff on 429/5xx."""

from __future__ import annotations

import time
from collections.abc import Iterator

import requests

from .settings import load_config

_session: requests.Session | None = None
_last_request = 0.0


def session() -> requests.Session:
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers["User-Agent"] = load_config()["user_agent"]
    return _session


def get_json(
    url: str, params: dict | None = None, *, max_tries: int = 8, min_interval: float | None = None
) -> dict:
    """GET a JSON document, sleeping between calls and backing off on throttling."""
    global _last_request
    if min_interval is None:
        min_interval = load_config().get("http", {}).get("min_interval_seconds", 1.0)
    for attempt in range(max_tries):
        wait = min_interval - (time.monotonic() - _last_request)
        if wait > 0:
            time.sleep(wait)
        _last_request = time.monotonic()
        resp = session().get(url, params=params, timeout=60)
        if resp.status_code == 404:
            return {}
        throttled = "too many requests" in resp.text[:300].lower()
        if resp.status_code == 429 or resp.status_code >= 500 or throttled:
            retry_after = resp.headers.get("Retry-After")
            time.sleep(float(retry_after) if retry_after else 2**attempt)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Gave up after {max_tries} tries: {url} {params}")


def mw_query(api: str, params: dict) -> Iterator[dict]:
    """Iterate over the pages of a MediaWiki action=query request, following `continue`."""
    base = {"action": "query", "format": "json", "formatversion": "2", **params}
    cont: dict = {}
    while True:
        data = get_json(api, {**base, **cont})
        yield data.get("query", {})
        if "continue" not in data:
            return
        cont = data["continue"]


def batched(items: list, size: int) -> Iterator[list]:
    for i in range(0, len(items), size):
        yield items[i : i + size]
