"""
Top-level agent entrypoint. Wires together:
  intent_parser.parse_intent() -> planner.build_plan() -> tools.*
routes.py should only ever need to call run_agent(query).
"""

from . import intent_parser
from . import planner
from . import tools

TOOL_DISPATCH = {
    "explain": tools.explainability_tool,
    "lookup": tools.get_customer_segment,
    "retention": tools.retention_tool,
    "eda": tools.eda_tool,
    "segment": tools.segmentation_tool,
}


def run_agent(query: str) -> dict:
    parsed = intent_parser.parse_intent(query)
    plan = planner.build_plan(parsed)

    if not plan["ready"]:
        return {
            "status": "needs_clarification",
            "message": plan["clarification"],
            "parsed_intent": parsed,
            "plan": plan,
        }

    tool_fn = TOOL_DISPATCH.get(plan["tool"])
    if tool_fn is None:
        return {
            "status": "error",
            "message": f"No tool wired up for action '{plan['tool']}'.",
            "parsed_intent": parsed,
            "plan": plan,
        }

    try:
        result = tool_fn(**plan["args"])
    except Exception as e:
        return {
            "status": "error",
            "message": f"Tool '{plan['tool']}' failed: {e}",
            "parsed_intent": parsed,
            "plan": plan,
        }

    if isinstance(result, dict) and "error" in result:
        return {
            "status": "error",
            "message": result["error"],
            "parsed_intent": parsed,
            "plan": plan,
        }

    return {
        "status": "ok",
        "action": plan["tool"],
        "result": result,
        "parsed_intent": parsed,
        "plan": plan,
    }
def to_chat_response(agent_result: dict) -> dict:
    """
    Formats a run_agent() result into the shape ChatResponse expects
    (response / execution_plan / results). Shared by routes.py's pure
    rule-based path and gemini_service.py's fallback path, so the two
    don't drift out of sync.
    """
    execution_plan = [
        f"Parsed query -> action: {agent_result['parsed_intent'].get('action') or 'unclear'}"
    ]

    if agent_result["parsed_intent"].get("customer_id") is not None:
        execution_plan.append(
            f"Extracted customer_id={agent_result['parsed_intent']['customer_id']}"
        )
    if agent_result["parsed_intent"].get("cluster") is not None:
        execution_plan.append(
            f"Extracted cluster={agent_result['parsed_intent']['cluster']}"
        )

    if agent_result["status"] == "ok":
        execution_plan.append(f"Called tool: {agent_result['action']}")
        return {
            "response": f"Here's what I found using the {agent_result['action']} tool.",
            "execution_plan": execution_plan,
            "results": agent_result["result"],
        }

    elif agent_result["status"] == "needs_clarification":
        execution_plan.append("Requested clarification from user")
        return {
            "response": agent_result["message"],
            "execution_plan": execution_plan,
            "results": {},
        }

    else:  # error
        execution_plan.append(f"Tool error: {agent_result['message']}")
        return {
            "response": f"Something went wrong: {agent_result['message']}",
            "execution_plan": execution_plan,
            "results": {},
        }