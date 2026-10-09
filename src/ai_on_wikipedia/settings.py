"""Load config.yaml and shared helpers for the observation window."""

from __future__ import annotations

from datetime import date
from functools import cache
from pathlib import Path

import yaml

CONFIG_PATH = Path("config.yaml")


@cache
def load_config(path: str | Path = CONFIG_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def period(month: date, boundary: date) -> str:
    """Label a month as 'pre' or 'post' relative to the period boundary (first post month)."""
    return "post" if month >= boundary else "pre"


def project_domain(wiki: str) -> str:
    """'en' -> 'en.wikipedia' (the form the Wikimedia REST API expects)."""
    return f"{wiki}.wikipedia"


def api_url(wiki: str) -> str:
    return f"https://{wiki}.wikipedia.org/w/api.php"
