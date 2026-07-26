"""
Groq-powered chat layer for POST /chat.

Uses Groq's OpenAI-compatible chat completions API with manual tool
calling: we hand Groq a JSON schema describing each tools.py function,
Groq decides which one (if any) to call and with what arguments, we
execute it locally in Python, then send the result back to Groq for a
natural-language summary.

Falls back to the deterministic rule-based agent (agent.run_agent) if:
  - GROQ_API_KEY isn't set in the environment
  - the Groq call raises for any reason (network, quota, bad response,
    auth failure, token-limit, etc.)

This means /chat keeps working with zero external dependency when no API
key is configured, or when Groq is temporarily unavailable -- Groq only
upgrades the experience, it is never a hard requirement.
"""

import os
import json

from . import tools
from . import agent as rule_based_agent
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL_NAME = os.environ.get("GROQ_MODEL_NAME", "llama-3.1-8b-instant")

# Max characters of a tool's raw JSON result to send back to Groq as
# context for the summary step. Some tools (eda_tool, segmentation_tool
# with no cluster filter) can return large payloads that blow past the
# free-tier tokens-per-minute limit -- this keeps the follow-up call
# small regardless of which tool ran.
_MAX_TOOL_RESULT_CHARS = 4000

SYSTEM_INSTRUCTION = (
    "You are a retail banking analytics assistant for a customer "
    "segmentation tool. Use the available tools to answer questions about "
    "customer segmentation, feature engineering, data preprocessing, "
    "EDA, customer segments, personas, retention risk, and individual "
    "customers. Always call a tool to get real numbers rather than "
    "guessing or estimating."
)

# Groq (OpenAI-compatible) requires an explicit JSON schema per tool --
# unlike the Gemini SDK, it does not auto-generate schemas from Python
# type hints. These must match tools.py's actual signatures exactly.
_TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "explainability_tool",
            "description": (
                "Explain why a specific customer was assigned to their "
                "cluster, comparing their attributes (income, balance, "
                "credit score, transactions, investment, digital score) "
                "against the cluster average."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The numeric ID of the customer to explain.",
                    },
                },
                "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_segment",
            "description": (
                "Look up which cluster/segment a specific customer belongs "
                "to and their basic segment info."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The numeric ID of the customer to look up.",
                    },
                },
                "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "retention_tool",
            "description": (
                "Analyze customer engagement and recommend customer retention, "
                "cross-selling, premium upgrades, investment opportunities, "
                "loan eligibility, and next-best banking actions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "cluster": {
                        "type": "integer",
                        "description": (
                            "Optional cluster number to filter retention "
                            "results to. Omit to get all clusters."
                        ),
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "eda_tool",
            "description": (
                "Get exploratory data analysis / summary statistics, "
                "optionally filtered to a single cluster. If no cluster is "
                "given, returns stats across all clusters."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "cluster": {
                        "type": "integer",
                        "description": (
                            "Optional cluster number to filter EDA results "
                            "to. Omit to get all clusters."
                        ),
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "segmentation_tool",
            "description": (
                "Summarize customer segments identified by K-Means clustering. "
                "Return personas, customer counts, business characteristics, "
                "average financial metrics, business value, and recommended "
                "banking products for each segment."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "feature_engineering_tool",
            "description": (
                "Explain the feature engineering and preprocessing pipeline "
                "used before K-Means customer segmentation."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
]

_TOOL_FN_MAP = {
    "explainability_tool": tools.explainability_tool,
    "get_customer_segment": tools.get_customer_segment,
    "retention_tool": tools.retention_tool,
    "eda_tool": tools.eda_tool,
    "segmentation_tool": tools.segmentation_tool,
    "feature_engineering_tool": tools.feature_engineering_tool,
}

_ACTION_TO_TOOL_NAME = {
    "explain": "explainability_tool",
    "lookup": "get_customer_segment",
    "retention": "retention_tool",
    "eda": "eda_tool",
    "segment": "segmentation_tool",
}

_client = None
_GROQ_AVAILABLE = False

if GROQ_API_KEY:
    try:
        from groq import Groq

        _client = Groq(api_key=GROQ_API_KEY)
        _GROQ_AVAILABLE = True
    except Exception:
        _client = None
        _GROQ_AVAILABLE = False


def _serialize_tool_result(raw_result) -> str:
    """
    Turns a tool's raw return value into a JSON string capped at
    _MAX_TOOL_RESULT_CHARS, so large payloads (e.g. eda_tool or
    segmentation_tool with no cluster filter) can't blow past Groq's
    tokens-per-minute limit on the follow-up summary call.
    """
    if raw_result is None:
        return "null"

    full = json.dumps(raw_result)
    if len(full) <= _MAX_TOOL_RESULT_CHARS:
        return full

    return full[:_MAX_TOOL_RESULT_CHARS] + "... (truncated for length)"


def _run_groq_turn(query: str) -> dict:
    """
    Sends the query to Groq with manual tool calling enabled. Raises on
    any failure so the caller can fall back to the rule-based agent --
    this function should never be responsible for producing a
    user-facing error message itself.
    """
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": query},
    ]

    first_response = _client.chat.completions.create(
        model=GROQ_MODEL_NAME,
        messages=messages,
        tools=_TOOL_SCHEMAS,
        tool_choice="auto",
    )

    choice = first_response.choices[0]
    tool_calls = choice.message.tool_calls

    if not tool_calls:
        return {
            "response": choice.message.content,
            "execution_plan": ["Groq answered directly without calling a tool"],
            "results": {},
        }

    # Execute the first tool call locally (matches the single-tool-per-turn
    # behavior of the previous Gemini implementation).
    call = tool_calls[0]
    tool_name = call.function.name
    try:
        tool_args = json.loads(call.function.arguments)
    except (json.JSONDecodeError, TypeError):
        tool_args = {}

    raw_result = None
    if tool_name in _TOOL_FN_MAP:
        try:
            raw_result = _TOOL_FN_MAP[tool_name](**tool_args)
        except Exception:
            raw_result = None

    # Feed the (size-capped) tool result back to Groq so it can write a
    # natural-language summary, matching the two-step behavior the Gemini
    # SDK did for us automatically.
    messages.append(choice.message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": call.id,
            "content": _serialize_tool_result(raw_result),
        }
    )

    second_response = _client.chat.completions.create(
        model=GROQ_MODEL_NAME,
        messages=messages,
    )

    summary_text = second_response.choices[0].message.content

    return {
        "response": summary_text,
        "execution_plan": [
            f"Groq selected tool: {tool_name}",
            "Groq summarized the result",
        ],
        # Note: the frontend still gets the FULL untruncated result here --
        # only the copy sent back to Groq for summarization is capped.
        "results": raw_result if isinstance(raw_result, (dict, list)) else {},
    }


def generate_chat_response(query: str) -> dict:
    """
    Main entrypoint for POST /chat. Tries Groq first (if configured),
    falls back to the deterministic rule-based agent on any failure.
    Always returns a dict shaped for ChatResponse -- never raises.
    """
    if _GROQ_AVAILABLE:
        try:
            return _run_groq_turn(query)
        except Exception as e:
            # print("GROQ ERROR:", repr(e))
            fallback_result = rule_based_agent.run_agent(query)
            formatted = rule_based_agent.to_chat_response(fallback_result)
            formatted["execution_plan"] = [
                f"Groq call failed ({e}); used rule-based fallback."
            ] + formatted["execution_plan"]
            return formatted

    fallback_result = rule_based_agent.run_agent(query)
    formatted = rule_based_agent.to_chat_response(fallback_result)
    if not GROQ_API_KEY:
        formatted["execution_plan"] = [
            "GROQ_API_KEY not set; used rule-based agent."
        ] + formatted["execution_plan"]
    return formatted