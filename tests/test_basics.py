from datetime import date
from pathlib import Path

import pytest

from ai_on_wikipedia.privacy import editor_key
from ai_on_wikipedia.settings import period
from ai_on_wikipedia.wp1 import load_wp1, narrow_titles

SNAPSHOT = Path("data/raw/wp1_artificial_intelligence_2026-10-09.tsv")


def test_period_boundary():
    boundary = date(2022, 11, 1)
    assert period(date(2022, 10, 1), boundary) == "pre"
    assert period(date(2022, 11, 1), boundary) == "post"


def test_editor_key_is_stable_and_salted():
    assert editor_key("ExampleUser", salt="a") == editor_key("ExampleUser", salt="a")
    assert editor_key("ExampleUser", salt="a") != editor_key("ExampleUser", salt="b")
    assert "ExampleUser" not in editor_key("ExampleUser", salt="a")


def test_editor_key_requires_salt(monkeypatch):
    monkeypatch.delenv("EDITOR_ID_SALT", raising=False)
    with pytest.raises(RuntimeError):
        editor_key("ExampleUser")


def test_wp1_snapshot_namespaces():
    df = load_wp1(SNAPSHOT)
    narrow = narrow_titles(df)
    # Reconciles with the counts recorded in DATA-DICTIONARY.md for this snapshot.
    assert len(df) == 1882
    assert len(narrow) == 1246
    assert not narrow["title"].str.startswith(("Draft:", "Category:", "Template:")).any()
    assert "-Class" not in "".join(narrow["quality"])
