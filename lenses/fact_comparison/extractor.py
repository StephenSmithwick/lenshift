import spacy
from bs4 import BeautifulSoup
from spacy.lang.en.stop_words import STOP_WORDS

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_facts_from_content(content):
    """Extracts facts from HTML content."""

    soup = BeautifulSoup(content, 'html.parser')

    # Find the main article text (this might need adjustment for different sites)
    # Find the main article content
    article_body = soup.find('article') or soup.find('div', class_='post-content')

    article_text = ''
    if article_body:
        paragraphs = article_body.find_all('p')
        if paragraphs:
            article_text = '\n'.join([p.get_text() for p in paragraphs])
        else:
            # If no paragraphs found within specific article body, get all text
            article_text = article_body.get_text(separator='\n', strip=True)
    else:
        # Fallback to body if no specific article body found
        body_element = soup.find('body')
        if body_element:
            paragraphs = body_element.find_all('p')
            if paragraphs:
                article_text = '\n'.join([p.get_text() for p in paragraphs])
            else:
                article_text = body_element.get_text(separator='\n', strip=True)
    title_element = soup.find('h1')
    title_text = title_element.get_text() if title_element else ''

    first_paragraph_element = None
    if article_body:
        first_paragraph_element = article_body.find('p')
    first_paragraph_text = first_paragraph_element.get_text() if first_paragraph_element else ''

    # Combine title and first paragraph for key entity extraction
    key_entity_text = title_text + " " + first_paragraph_text
    key_entity_doc = nlp(key_entity_text)

    if not article_text:
        return {"error": "Could not find article text."}

    doc = nlp(article_text)

    # Normalize text function
    def normalize_text(text):
        # Keep only alphanumeric characters and spaces, and convert to lowercase
        text = ''.join(char.lower() for char in text if char.isalnum() or char.isspace())
        # Remove stopwords, but keep the entity if it's a single word that happens to be a stopword
        words = text.split()
        if len(words) > 1:
            return ' '.join([word for word in words if word not in STOP_WORDS])
        return text

    # Extract named entities from the entire article
    entities = {
        "people": sorted(list(set([ent.text for ent in doc.ents if ent.label_ == 'PERSON']))),
        "organizations": sorted(list(set([ent.text for ent in doc.ents if ent.label_ == 'ORG']))),
        "locations": sorted(list(set([ent.text for ent in doc.ents if ent.label_ == 'GPE' or ent.label_ == 'LOC']))),
        "dates": sorted(list(set([ent.text for ent in doc.ents if ent.label_ == 'DATE']))),
    }

    # Prioritize dates that are more specific (e.g., contain month, day, or year)
    primary_date = None
    if entities['dates']:
        # Simple scoring system: prefer dates with numbers (years, days)
        def date_score(date_text):
            score = 0
            if any(char.isdigit() for char in date_text):
                score += 1
            if any(day in date_text.lower() for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
                score += 1
            if any(month in date_text.lower() for month in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]):
                score += 1
            return score

        # Sort dates by score, then by length
        sorted_dates = sorted(entities['dates'], key=lambda d: (date_score(d), len(d.split())), reverse=True)
        primary_date = sorted_dates[0] if sorted_dates else None

    event_fingerprint = {
        "key_entities": sorted(list(set([normalize_text(ent.text) for ent in key_entity_doc.ents if normalize_text(ent.text)]))), # All entities from title/first paragraph, normalized and filtered
        "primary_date": primary_date,
    }

    return {
        "event_fingerprint": event_fingerprint,
        "facts": entities
    }
