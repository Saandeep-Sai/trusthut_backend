import re
from apps.core.firebase import get_firestore_client
from apps.core.config import POSTS_COLLECTION


# Common stop words to filter out during keyword extraction
STOP_WORDS = {
    'is', 'are', 'was', 'were', 'the', 'a', 'an', 'in', 'on', 'at', 'to',
    'for', 'of', 'and', 'or', 'but', 'not', 'with', 'from', 'by', 'it',
    'this', 'that', 'how', 'what', 'where', 'when', 'who', 'which', 'can',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
    'has', 'have', 'had', 'be', 'been', 'being', 'there', 'here', 'about',
    'i', 'me', 'my', 'we', 'our', 'you', 'your', 'they', 'them', 'their',
}


def extract_keywords(query):
    """Extract meaningful keywords from a user query."""
    words = re.findall(r'\w+', query.lower())
    keywords = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return keywords


def search_related_posts(keywords):
    """Search Firestore for posts matching any of the keywords."""
    db = get_firestore_client()
    all_docs = db.collection(POSTS_COLLECTION).stream()

    results = []
    for doc in all_docs:
        data = doc.to_dict()
        searchable = (
            f"{data.get('title', '')} "
            f"{data.get('description', '')} "
            f"{data.get('location_name', '')}"
        ).lower()

        score = sum(1 for kw in keywords if kw in searchable)
        if score > 0:
            data['_relevance_score'] = score
            results.append(data)

    # Sort by relevance
    results.sort(key=lambda x: x['_relevance_score'], reverse=True)

    # Remove internal score and return top matches
    for r in results:
        r.pop('_relevance_score', None)

    return results[:10]


def generate_summary(query, related_posts):
    """Generate a text summary based on related posts."""
    if not related_posts:
        return "I don't have enough reports about this area yet. Try searching for a different location or topic."

    total = len(related_posts)
    safe_count = sum(1 for p in related_posts if p.get('risk_level') == 'safe')
    moderate_count = sum(1 for p in related_posts if p.get('risk_level') == 'moderate')
    unsafe_count = sum(1 for p in related_posts if p.get('risk_level') == 'unsafe')

    # Collect accessibility types mentioned
    types = set(p.get('accessibility_type', '') for p in related_posts)
    types_str = ', '.join(t for t in types if t)

    # Collect unique locations mentioned
    locations = set(p.get('location_name', '') for p in related_posts)
    locations_str = ', '.join(l for l in locations if l)

    # Build summary
    summary_parts = [f"Based on {total} report(s) found:"]

    if safe_count:
        summary_parts.append(f"✅ {safe_count} report(s) marked as safe.")
    if moderate_count:
        summary_parts.append(f"⚠️ {moderate_count} report(s) marked as moderate risk.")
    if unsafe_count:
        summary_parts.append(f"🚫 {unsafe_count} report(s) marked as unsafe.")

    if types_str:
        summary_parts.append(f"Accessibility concerns: {types_str}.")
    if locations_str:
        summary_parts.append(f"Locations mentioned: {locations_str}.")

    # Overall assessment
    if unsafe_count > safe_count:
        summary_parts.append("⚠️ Overall, this area may have significant accessibility challenges. Please proceed with caution.")
    elif safe_count > unsafe_count:
        summary_parts.append("✅ Overall, this area appears to be relatively accessible based on reports.")
    else:
        summary_parts.append("ℹ️ Mixed reports — consider checking specific locations for more details.")

    return ' '.join(summary_parts)


def process_query(query):
    """Main chatbot pipeline: extract → search → summarize → respond."""
    keywords = extract_keywords(query)

    if not keywords:
        return {
            'answer': "I couldn't understand your question. Try asking about a specific location or accessibility concern.",
            'related_posts': [],
        }

    related_posts = search_related_posts(keywords)
    answer = generate_summary(query, related_posts)

    # Return simplified post data for the response
    simplified_posts = [
        {
            'post_id': p.get('post_id'),
            'title': p.get('title'),
            'location_name': p.get('location_name'),
            'risk_level': p.get('risk_level'),
            'accessibility_type': p.get('accessibility_type'),
        }
        for p in related_posts[:5]
    ]

    return {
        'answer': answer,
        'related_posts': simplified_posts,
    }
