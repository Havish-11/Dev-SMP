# Multi-Agent Log Analyzer

A multi-agent pipeline that analyzes server logs, classifies issues, suggests fixes, and validates them — powered by **Groq** (LLaMA 3).

## Agents

| Agent | Role |
|---|---|
| `LogAnalysisAgent` | Parses raw logs into structured entries |
| `IssueClassificationAgent` | Groups errors into typed issues with severity |
| `FixSuggestionAgent` | Proposes shell commands to fix each issue |
| `ValidationAgent` | Reviews commands for safety before approval |
| `OrchestratorAgent` | Drives the full pipeline end to end |

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Groq API key (free at https://console.groq.com)
cp .env.example .env
# Edit .env and paste your key

# 3. Run with sample logs
python main.py

# 4. Or pass your own log file
python main.py /var/log/app.log

# 5. Or pipe logs directly
tail -n 100 /var/log/syslog | python main.py
```

## Changing the Model

Edit `MODEL` in `agents/base_agent.py`:

| Model | Speed | Quality | Context |
|---|---|---|---|
| `llama-3.1-8b-instant` | ⚡ Fastest | Good | 128k |
| `llama-3.3-70b-versatile` | Fast | Best | 128k |
| `mixtral-8x7b-32768` | Fast | Great | 32k |

## Project Structure

```
log-analyzer/
├── agents/
│   ├── base_agent.py            # Groq client + shared helpers
│   ├── log_analysis_agent.py
│   ├── issue_classification_agent.py
│   ├── fix_suggestion_agent.py
│   ├── validation_agent.py
│   └── orchestrator_agent.py
├── models/
│   └── schemas.py               # Pydantic models
├── utils/
│   └── message_bus.py           # Async inter-agent messaging
├── main.py
├── requirements.txt
└── .env.example
```
