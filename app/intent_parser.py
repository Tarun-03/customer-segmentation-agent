import re

ACTION_KEYWORDS = {
    "explain": ["why", "explain", "basis", "reason", "criteria", "how were", "on what basis"],
    "retention": ["at risk", "retention", "churn", "disengag", "convert", "conversion", "dormant", "re-engage"],
    "eda": ["average", "distribution", "missing", "correlation", "how many", "count", "overview", "explore", "profile the data"],
    "segment": ["segment", "cluster", "group", "persona"],
    "lookup": ["is customer", "customer id", "customer #"]
}


def _load_persona_lookup():
    from . import tools
    personas = tools._load_personas()
    return {row["persona"].lower(): int(row["cluster"]) for _, row in personas.iterrows()}


def _extract_customer_id(query: str):
    match = re.search(r"customer\s*(?:id)?\s*#?\s*(\d+)", query, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def _extract_cluster(query: str):
    match = re.search(r"cluster\s*(\d+)", query, re.IGNORECASE)
    if match:
        return int(match.group(1))

    persona_lookup = _load_persona_lookup()
    query_lower = query.lower()
    for persona_name, cluster_num in persona_lookup.items():
        if persona_name in query_lower:
            return cluster_num

    return None


def _detect_action(query: str):
    query_lower = query.lower()

    segment_creation_phrases = ["segment customers into", "cluster customers into", "group customers into"]
    for phrase in segment_creation_phrases:
        if phrase in query_lower:
            return "segment"

    for action in ["explain", "retention", "eda", "lookup", "segment"]:
        for keyword in ACTION_KEYWORDS[action]:
            if keyword in query_lower:
                return action

    return None


def parse_intent(query: str):
    customer_id = _extract_customer_id(query)
    cluster = _extract_cluster(query)
    action = _detect_action(query)

    if action is None and customer_id is not None:
        action = "lookup"

    needs_clarification = action is None

    return {
        "raw_query": query,
        "action": action,
        "customer_id": customer_id,
        "cluster": cluster,
        "needs_clarification": needs_clarification
    }