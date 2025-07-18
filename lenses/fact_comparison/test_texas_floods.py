import pytest
import vcr
from main import fetch_content, extract_facts_from_content, compare_articles

@vcr.use_cassette(cassette_library_dir='lenses/fact_comparison/cassettes')
def test_texas_floods_fact_comparison():
    url1 = "https://www.nbcnews.com/news/us-news/texas-flood-hometown-lifetime-tragedy-rcna217210"
    url2 = "https://www.cnn.com/weather/live-news/texas-flooding-camp-mystic-07-07-25-hnk"

    content1 = fetch_content(url1)
    content2 = fetch_content(url2)

    assert content1 is not None, "Failed to fetch content for URL 1"
    assert content2 is not None, "Failed to fetch content for URL 2"

    facts1 = extract_facts_from_content(content1)
    facts2 = extract_facts_from_content(content2)

    assert "error" not in facts1, f"Fact extraction failed for URL 1: {facts1.get('error')}"
    assert "error" not in facts2, f"Fact extraction failed for URL 2: {facts2.get('error')}"

    comparison_result = compare_articles(facts1, facts2)

    assert comparison_result["articles_cover_same_event"] is True, "Articles were not identified as covering the same event"
