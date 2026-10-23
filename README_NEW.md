# TaskRoute AI

**An intelligent task-routing assistant that uses Strands Decider 2B to classify programming questions and route them to specialized tools.**

## 🎯 What It Does

TaskRoute AI doesn't just answer programming questions—it routes them intelligently. When you ask a question, Strands Decider 2B makes a calibrated decision to select the best tool:

- **debug_tool**: For syntax errors, runtime exceptions, and debugging strategies
- **learn_tool**: For explanations of algorithms, language features, and programming concepts  
- **career_tool**: For interview prep, resume advice, and job search strategies

Instead of a one-size-fits-all LLM, TaskRoute AI provides **specialized assistance** with **measured confidence** and **intelligent fallback** for uncertain cases.

## 🏗️ Architecture

```
User Input
    ↓
Strands Decider 2B (makes tool-selection decision)
    ├─ Confidence ≥ 0.6 → Route to specific tool
    └─ Confidence < 0.6 → Ask clarifying question
    ↓
Amazon Bedrock LLM (Qwen3.5 or Nova Pro)
    ↓
Specialized Response
```

## 📊 Real Performance Metrics

### Tool Selection Accuracy (Test Split)
- **Debug Tool**: 97.1% confidence on error-related queries
- **Learn Tool**: 82.0% confidence on concept questions
- **Career Tool**: 80.3% confidence on interview/job questions
- **Low-Confidence Handling**: Correctly identifies ambiguous queries <60% confidence

### Latency
- **Strands Decider 2B**: ~2,000ms per decision (hosted API)
- **Amazon Bedrock LLM**: ~3-5 seconds per response
- **End-to-End**: ~5-7 seconds from input to response

### Reusable Decision Pattern
- **Pattern**: #tool-selection (REUSABLE DECISION PATTERN in agent/decision.py)
- **Model**: StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 (Apache-2.0)
- **Questions**: Single `choice` type with 4 options (3 tools + none)
- **Threshold**: 0.6 (decisions above this narrow to one tool)
- **Eval Cases**: 24 labeled cases (12 tune, 12 test) covering all three categories

## 🚀 Quick Start

### Local Development
```bash
# Prerequisites
python 3.12+
.venv virtual environment (auto-created by kit)

# Install dependencies
pip install -r requirements.txt

# Run tests
./kit test

# Start demo UI
./kit demo-bg
# Open http://localhost:8501
```

### Deployment to AWS
```bash
./kit deploy                          # Deploy to Bedrock AgentCore Runtime
./kit invoke "Your question here"     # Test deployed agent
./kit video --target agentcore        # Record video on deployed agent
./kit destroy                         # Clean up when done
```

## 🧪 Testing

**All 38 tests pass:**
```
38 passed in 14.85s
```

**Test Coverage:**
- ✅ Agent interface contract
- ✅ Decision pattern labeling and questions
- ✅ Eval case matching
- ✅ Tool execution
- ✅ LLM provider routing
- ✅ Image handling
- ✅ Security (no hardcoded secrets)

## 🎯 How to Reuse the Decision Pattern

This #tool-selection pattern is designed for reuse. To adapt it to your domain:

1. **Copy** `agent/decision.py` (TaskRouter class)
2. **Define** your domain-specific tools with clear docstrings
3. **Adjust** the decision threshold for your use case
4. **Integrate** TaskRouter before agent LLM inference:
   ```python
   from agent.decision import TaskRouter
   router = TaskRouter(decider, tools, threshold=0.6)
   selected_tools = router.select_tools(user_message)
   agent = Agent(model=..., tools=selected_tools, ...)
   ```

## 📁 Project Structure

```
agent/
  AGENT.md              # Use case description
  decision.py           # REUSABLE DECISION PATTERN: #tool-selection
  tools.py              # debug_tool, learn_tool, career_tool
  agent.py              # HackathonAgent with TaskRouter integration
  eval_cases.jsonl      # 24 labeled test cases (12 tune, 12 test)
  demo_script.yaml      # Demo video script for kit video
  features.yaml         # AgentCore features config (Memory/Gateway)

decider_kit/
  patterns/             # 5 reusable decision patterns
  bench.py              # Benchmark framework
  llm.py                # LLM provider routing (Bedrock/local/UGMDU)
  client.py             # Strands Decider 2B client

submission/
  bench/                # Benchmark results
  video/                # Demo video (demo.mp4)
  article/              # Article content and cover image
```

## 🔐 Security

- ✅ No secrets in source code (.env is gitignored)
- ✅ AWS credentials loaded from environment
- ✅ Bedrock API keys never logged
- ✅ All inputs validated

## 📝 Built With

- **Strands Agents SDK** — Agent orchestration and tool calling
- **Strands Decider 2B** — Calibrated decision model (Apache-2.0)
- **Amazon Bedrock** — Generative AI (Amazon Nova Pro)
- **AWS User Group Madurai Hackathon Kit** — Scaffolding, deployment, benchmark framework

---

**Built with the AWS User Group Madurai Strands Decider hackathon kit**

Tags: `#strands-decider-2b` `#tool-selection`
