# Current Approach for Article Fact Comparison

This document outlines the current architecture and tools used for the article fact comparison feature in Lenshift.

## Goal
To identify articles covering the same event, extract key facts, and highlight differences in a machine-readable format (JSON).

## Development Environment
- **Virtual Environment**: All development and execution should be done within the Python virtual environment located in the `.venv/` directory. To activate it, run `source .venv/bin/activate`. **[Loaded]**
- **Package Management**: `uv` is the preferred tool for managing Python packages. All dependencies should be installed using `uv pip install`.

## Components

### 1. Fact Extraction (`lenses/fact_comparison/extractor.py`)
- **Purpose**: Parses HTML content to extract named entities and create an event fingerprint.
- **Libraries Used**:
    - `requests`: For fetching HTML content from URLs.
    - `BeautifulSoup4`: For parsing HTML and extracting article text.
    - `spaCy`: For Natural Language Processing (NLP), specifically Named Entity Recognition (NER) to identify people, organizations, locations, and dates.
- **Output**: A dictionary containing:
    - `event_fingerprint`: Includes `key_entities` (normalized entities from title/first paragraph) and `primary_date`.
    - `facts`: Categorized lists of extracted entities (people, organizations, locations, dates).

### 2. Fact Comparison (`lenses/fact_comparison/comparator.py`)
- **Purpose**: Compares facts extracted from two articles to determine if they cover the same event and identifies common and unique facts.
- **Logic**:
    - Checks if articles cover the same event based on `primary_date` and common `key_entities` from their fingerprints.
    - If they cover the same event, it categorizes facts into `common_facts`, `unique_facts_article1`, and `unique_facts_article2` for 'people', 'organizations', 'locations', and 'dates'.
- **Output**: A dictionary summarizing the comparison, including a boolean `articles_cover_same_event` and categorized common/unique facts.

## Workflow
1. Two URLs are provided as command-line arguments.
2. `main.py` fetches the HTML content from the URLs.
3. `extractor.py` processes the HTML to get facts and an event fingerprint for each article.
4. `comparator.py` takes the extracted facts from two articles and performs the comparison.
5. The comparison result is a dictionary, which is serialized to JSON and printed to the console.

## Next Steps
- Refine the fact extraction process to handle different article structures.
- Improve the event fingerprinting logic for more accurate event matching.
- Add more sophisticated NLP analysis to understand the context of the facts.
