def compare_articles(article1_facts, article2_facts):
    """Compares facts between two articles and highlights differences."""
    comparison_result = {
        "articles_cover_same_event": False,
        "common_facts": {
            "people": [],
            "organizations": [],
            "locations": [],
            "dates": []
        },
        "unique_facts_article1": {
            "people": [],
            "organizations": [],
            "locations": [],
            "dates": []
        },
        "unique_facts_article2": {
            "people": [],
            "organizations": [],
            "locations": [],
            "dates": []
        }
    }

    # Check if articles cover the same event based on fingerprint
    fp1 = article1_facts.get("event_fingerprint", {})
    fp2 = article2_facts.get("event_fingerprint", {})

    # More flexible check: if primary dates exist and there's a significant overlap in key entities
    if fp1.get("primary_date") and fp2.get("primary_date"):
        set1 = set(fp1.get("key_entities", []))
        set2 = set(fp2.get("key_entities", []))
        
        # Require at least 2 common key entities or a high percentage of overlap
        common_count = len(set1.intersection(set2))
        if common_count >= 2 or (len(set1) > 0 and common_count / len(set1) > 0.5):
            comparison_result["articles_cover_same_event"] = True

    # Compare facts if they cover the same event
    if comparison_result["articles_cover_same_event"]:
        categories = ["people", "organizations", "locations", "dates"]
        for category in categories:
            set1 = set(article1_facts["facts"].get(category, []))
            set2 = set(article2_facts["facts"].get(category, []))

            comparison_result["common_facts"][category] = sorted(list(set1.intersection(set2)))
            comparison_result["unique_facts_article1"][category] = sorted(list(set1.difference(set2)))
            comparison_result["unique_facts_article2"][category] = sorted(list(set2.difference(set1)))

    return comparison_result