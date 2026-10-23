"""REUSABLE DECISION PATTERN: TOOL SELECTION  (#tool-selection)

What it does
    TaskRoute AI uses Strands Decider 2B to route user questions to the most appropriate tool.
    Given a programming-related question, the decider selects exactly one of three tools:
    - debug_tool: programming errors and debugging
    - learn_tool: explanations of programming concepts
    - career_tool: interview and placement preparation
    
    If confidence is too low (< 0.6), the agent keeps all tools and asks the LLM to choose.
    If the input is unclear, the agent asks a clarifying question instead of guessing.

Typed questions and options
    tool (choice): one option per tool, described by the tool's own docstring, plus "none"
    ("no tool is needed, answer directly").

Wiring
    TaskRouter is integrated into HackathonAgent in agent/agent.py. It sits between the
    user message and the LLM agent, selecting which tools to provide based on the decider's
    decision.

How to reuse it
    Copy this file, change TOOLS to your own tools, and adjust the threshold as needed.
    The pattern automatically reads tool descriptions from docstrings.
"""

from __future__ import annotations

from typing import Any

from decider_kit import Decider
from decider_kit.patterns.tool_selection import ToolSelector

IS_KIT_EXAMPLE = False  # This is our original agent
PATTERN_TAG = "#tool-selection"


class TaskRouter:
    """Tool selection router for TaskRoute AI."""
    
    def __init__(self, decider: Decider, tools: list[Any], threshold: float = 0.6):
        self.selector = ToolSelector(decider, tools, threshold, context="Choose the tool that best fits this programming-related question.")
        self.log: list[dict[str, Any]] = []
    
    def select_tools(self, request: str, history: str = "") -> tuple[list[Any], dict[str, Any]]:
        """Select which tools to use for this request.
        
        Returns:
            tuple: (list of selected tools, decision log entry)
        """
        selection = self.selector.select(request, history)
        
        # Log the decision
        log_entry = {
            "pattern": PATTERN_TAG,
            "stage": "tool_selection",
            "selected_tool": selection.tool,
            "confidence": round(selection.confidence, 3),
            "narrowed": selection.narrowed,
            "probabilities": {k: round(v, 3) for k, v in selection.decision.probabilities.items()},
            "decider_ms": self.selector.decider.last_latency_ms,
            "user_request": request[:100] + ("..." if len(request) > 100 else "")
        }
        self.log.append(log_entry)
        
        # Get tools based on selection
        selected_tools = self.selector.tools_for(request, history)
        
        return selected_tools, log_entry
    
    def get_decision_feedback(self, confidence: float, selected_tool: str) -> str | None:
        """Generate feedback for low-confidence decisions.
        
        If confidence is too low, suggest asking a clarifying question.
        """
        if confidence < 0.4:
            return "I'm not sure which type of help you need. Could you clarify: are you asking about a specific error, learning a concept, or career advice?"
        elif confidence < 0.6:
            return f"I think you might need help with {selected_tool.replace('_', ' ')}. Is that correct, or would you like me to consider other types of help?"
        return None


# Questions for evaluation cases (maintains compatibility with test suite)
# Note: Actual tool selection uses dynamic questions based on tool docstrings
from decider_kit import Decider

QUESTIONS = {
    "tool": Decider.choice(
        "Which tool should handle this programming-related request?",
        {
            "debug_tool": "programming errors and debugging",
            "learn_tool": "explanations of programming concepts", 
            "career_tool": "interview and placement preparation",
            "none": "no tool is needed; the assistant can answer directly"
        }
    )
}