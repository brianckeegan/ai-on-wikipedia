"""Pseudonymize editor identifiers at ingest.

Usernames and IP addresses are personal data even though Wikipedia publishes them. They are
replaced with a keyed hash (HMAC-SHA256) before anything is written to data/interim/; the key
(EDITOR_ID_SALT) lives only in .env and is never committed or released.
"""

from __future__ import annotations

import hashlib
import hmac
import os


def editor_key(identifier: str, salt: str | None = None) -> str:
    """Stable pseudonym for an editor; the same identifier and salt always give the same key."""
    salt = salt if salt is not None else os.environ.get("EDITOR_ID_SALT", "")
    if not salt:
        raise RuntimeError("EDITOR_ID_SALT is not set; copy .env.example to .env and set it.")
    return hmac.new(salt.encode(), identifier.encode(), hashlib.sha256).hexdigest()[:16]
