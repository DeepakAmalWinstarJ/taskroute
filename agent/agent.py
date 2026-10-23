"""The agent: an LLM does the talking (Amazon Bedrock by default), Strands Decider 2B makes the decision.

TaskRoute AI: An intelligent task-routing assistant that uses Strands Decider 2B to select
the right tool for programming questions.

    from agent.agent import HackathonAgent
    out = HackathonAgent().chat("I'm getting a syntax error in my Python code")
    out["reply"], out["decisions"]
"""

from __future__ import annotations

import time
from typing import Any

from strands import Agent

from decider_kit import Decider
from decider_kit.llm import agent_model, default_model_id, image_blocks, strip_thinking

from .decision import TaskRouter
from .tools import TOOLS

NAME = "TaskRoute AI: Smart programming assistance router"
SYSTEM_PROMPT = """You are TaskRoute AI, a helpful assistant that routes programming questions to specialized tools.

You have access to three specialized tools:
1. debug_tool: For programming errors and debugging help
2. learn_tool: For explanations of programming concepts
3. career_tool: For interview preparation and career advice

When a user asks a question:
1. Use the appropriate tool if one was selected for you
2. If no tool was selected, answer directly using your knowledge
3. Be clear, helpful, and professional
4. If you need more information to use a tool properly, ask for it

Remember: You're here to help with programming-related questions. Stay on topic and provide practical advice."""


class HackathonAgent:
    """One Strands agent per session, with the tool selection pattern wired in."""

    def __init__(self, decider: Decider | None = None, model_id: str | None = None, eager: bool | None = None):
        import os

        self.decider = decider or Decider()
        self.eager = eager if eager is not None else os.environ.get("DEMO_EAGER") == "1"
        self.model_id = model_id or default_model_id()  # LLM_PROVIDER in .env: bedrock, local, ugmdu
        self.sessions: dict[str, TaskRouter] = {}



    def chat(self, message: str, session_id: str = "default", images: list[Any] | None = None) -> dict[str, Any]:
        """`images` (optional): photos the user attached (paths, bytes or base64); the LLM sees them
        as Strands image blocks. A decision that looks at them passes the same list to Decider.ask."""
        # Get or create router for this session
        if session_id not in self.sessions:
            self.sessions[session_id] = TaskRouter(self.decider, TOOLS, threshold=0.6)
        
        router = self.sessions[session_id]
        
        # Select tools for this message (adds decision to router.log)
        selected_tools, _ = router.select_tools(message)
        
        # Check if we should ask for clarification instead of proceeding
        if router.log:
            latest_decision = router.log[-1]
            confidence = latest_decision.get("confidence", 0)
            selected_tool = latest_decision.get("selected_tool", "")
            
            feedback = router.get_decision_feedback(confidence, selected_tool)
            if feedback and confidence < 0.6:
                # Low confidence - ask for clarification instead of using tools
                return {
                    "reply": feedback,
                    "decisions": router.log[-1:],  # Return the latest decision
                    "model_id": self.model_id,
                    "latency_ms": 0,
                    "agent": NAME,
                    "eager": self.eager,
                    "clarification_asked": True
                }
        
        # Create agent with selected tools
        agent = Agent(
            model=agent_model(self.model_id),
            system_prompt=SYSTEM_PROMPT,
            tools=selected_tools,
            interventions=[],  # No interventions needed for tool selection pattern
            callback_handler=None
        )
        
        t0 = time.perf_counter()
        
        # the LLM sees the photos as image blocks
        result = agent([*image_blocks(images), {"text": message}] if images else message,
                       invocation_state={"images": list(images or [])})
        reply = strip_thinking(str(result))  # Nova's <thinking>, Qwen's <think>
        
        return {
            "reply": reply,
            "decisions": router.log[-1:],  # Return the tool selection decision
            "model_id": self.model_id,
            "latency_ms": round((time.perf_counter() - t0) * 1000),
            "agent": NAME,
            "eager": self.eager,
            "clarification_asked": False
        }


if __name__ == "__main__":
    import json
    import sys

    a = HackathonAgent()
    
    # Test cases for each tool category
    test_messages = [
        "I'm getting 'SyntaxError: invalid syntax' in Python",
        "Can you explain what object-oriented programming is?",
        "How should I prepare for a software engineering interview?",
        "What does this error mean: 'TypeError: unsupported operand type(s)'?"
    ]
    
    for msg in sys.argv[1:] or test_messages:
        print(f"\n{'='*60}")
        print(f"Input: {msg}")
        print(f"{'='*60}")
        result = a.chat(msg)
        print(json.dumps(result, indent=2))
        
        # Print a summary
        if result.get("clarification_asked"):
            print("\n✓ Asked for clarification (low confidence)")
        elif result["decisions"]:
            decision = result["decisions"][0]
            print(f"\n✓ Selected tool: {decision.get('selected_tool', 'none')}")
            print(f"✓ Confidence: {decision.get('confidence', 0):.3f}")
            print(f"✓ Latency: {result['latency_ms']} ms")