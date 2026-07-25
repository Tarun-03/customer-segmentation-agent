"""
Quick manual test harness for agent.py — not wired into routes/main.
Run from project root: python test_agent.py
"""

from app.agent import run_agent

TEST_QUERIES = [
    # --- Should resolve and call a tool ---
    ("Show me an overview of the data", "eda"),
    ("What's the average income for cluster 1?", "eda"),
    ("Segment the customers into personas", "segment"),
    ("Why is customer 104 in this cluster?", "explain"),
    ("Show me at-risk customers in cluster 2", "retention"),
    ("Which customers are churning?", "retention"),
    ("Customer id 42", "lookup"),

    # --- Should trigger clarification (missing customer_id) ---
    ("Explain why this customer is grouped here", None),
    ("Is customer in this segment?", None),

    # --- Should trigger clarification (unrecognized intent) ---
    ("What's the weather today?", None),
]

def main():
    for query, expected_action in TEST_QUERIES:
        print("=" * 70)
        print(f"QUERY: {query}")
        result = run_agent(query)
        print(f"STATUS: {result['status']}")
        if result["status"] == "needs_clarification":
            print(f"CLARIFICATION: {result['message']}")
        elif result["status"] == "error":
            print(f"ERROR: {result['message']}")
        else:
            print(f"ACTION: {result['action']}")
            # Just print a short preview, not the full payload
            preview = str(result["result"])
            print(f"RESULT PREVIEW: {preview[:300]}")

        if expected_action is not None:
            actual = result.get("action") or result.get("parsed_intent", {}).get("action")
            match = "✅" if actual == expected_action else "❌ MISMATCH"
            print(f"EXPECTED: {expected_action} | GOT: {actual} {match}")

if __name__ == "__main__":
    main()