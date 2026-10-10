import pytest

from ai_on_wikipedia.frame import (
    qid_from_iri,
    sitelinks_query,
    sparql_string,
    titles_query,
    wiki_from_site,
)


def test_sparql_string_escapes_quotes_and_backslashes():
    assert sparql_string("ChatGPT", "en") == '"ChatGPT"@en'
    assert sparql_string('He said "hi"', "en") == '"He said \\"hi\\""@en'
    assert sparql_string("a\\b", "en") == '"a\\\\b"@en'


def test_titles_query_targets_one_wiki():
    q = titles_query(["GPT-4", "Python (programming language)"], "en")
    assert '"GPT-4"@en' in q
    assert '"Python (programming language)"@en' in q
    assert "<https://en.wikipedia.org/>" in q


def test_sitelinks_query_lists_items_and_sites():
    q = sitelinks_query(["Q1", "Q2"], ["en", "zh"])
    assert "wd:Q1 wd:Q2" in q
    assert "<https://en.wikipedia.org/>, <https://zh.wikipedia.org/>" in q


def test_iri_parsers():
    assert qid_from_iri("http://www.wikidata.org/entity/Q115564437") == "Q115564437"
    assert wiki_from_site("https://ko.wikipedia.org/") == "ko"
    with pytest.raises(ValueError):
        wiki_from_site("https://www.wikidata.org/")
