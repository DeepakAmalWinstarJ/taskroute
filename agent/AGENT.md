# Use case

**TaskRoute AI: A smart task-routing assistant for programming help.**

- **Pitch:** An AI assistant that intelligently routes programming questions to specialized tools using Strands Decider 2B for accurate tool selection.
- **Who it is for:** Developers, students, and job seekers who need programming help but don't know which type of assistance they need.
- **Features:**
  - Automatically categorizes questions into debugging, learning, or career advice
  - Uses Strands Decider 2B for fast, accurate tool selection
  - Provides specialized assistance from three targeted tools
  - Asks clarifying questions when uncertain instead of guessing
  - Clean web interface with real-time decision visualization
  - Deployed on Amazon Bedrock AgentCore Runtime
- **The decision handed to Strands Decider 2B:** Which specialized tool should handle this programming question? (`#tool-selection`)
- **Why a decision model:** Tool selection needs to be fast, consistent, and calibrated. A decision model provides probabilities that allow intelligent fallback (keeping all tools when unsure) and prevents wrong tool usage.
- **Amazon Bedrock:** The conversation and tool use (Qwen3.5:4b locally during development, Amazon Nova Pro for deployment).