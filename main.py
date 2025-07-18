#!/Users/steve/git/lenshift/.venv/bin/python3
import requests
import json
import sys
from lenses.fact_comparison.extractor import extract_facts_from_content
from lenses.fact_comparison.comparator import compare_articles

def fetch_content(url):
    """Fetches content from a URL."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <url1> <url2>")
        sys.exit(1)

    url1 = sys.argv[1]
    url2 = sys.argv[2]

    content1 = fetch_content(url1)
    content2 = fetch_content(url2)

    if not content1 or not content2:
        sys.exit(1)

    facts1 = extract_facts_from_content(content1)
    facts2 = extract_facts_from_content(content2)

    print("--- Facts from Article 1 ---")
    print(json.dumps(facts1, indent=2))
    print("--- Facts from Article 2 ---")
    print(json.dumps(facts2, indent=2))

    if "error" in facts1:
        print(f"Error extracting facts from article 1: {facts1['error']}")
        return
    if "error" in facts2:
        print(f"Error extracting facts from article 2: {facts2['error']}")
        return

    comparison_result = compare_articles(facts1, facts2)

    print(json.dumps(comparison_result, indent=2))

if __name__ == "__main__":
    main()