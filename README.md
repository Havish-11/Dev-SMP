I was not able to use the Gemini api keys. So I have used Groq API. Please excuse me for this

## Base Agent file

It holds the single shared Groq client and also registers the agent on the MessageBus at construction time.
Also I have set the max_toxens = 4096 and raises a clear Runtime Error if the model hits the token limit.


## Log Analysis Agent

It turns unstructured text into structured data. It send raw log to the LLM with a strict JSON schema prompt. Counts total errors and warnings, etc.

## Issue Classification Agent

It reads all the log entries and identifies patterns. Assigns each issue a severity level: low, medium, high or critical.
Also returns the frequency of occurence of each error.

## Fix Suggestion Agent

Reads the issue type, severity, description, and frequency. Generates a list of actionable shell commands (e.g. restart a service, free disk space, renew a certificate).
Self-assigns a confidence score (0.0–1.0) and a risk_level (low, medium, or high).

## Validation Agent

Reviews each shell command for destructive, irreversible, or privilege-escalating operations.
Flags anything suspicious as a warning. A fix can be is_safe=True but approved=False if it needs human review first.

## Orchestrator Agent

Instantiates all four specialist agents at startup.
Calls them in order: LogAnalysis → Classification → Fix → Validate.
Runs the Fix + Validate loop once per classified issue (not once per log line).
Collects all results into a dict[error_type, WorkflowResult] and returns it to main.py.

## Message Bus

An async pub/sub system that agents can use to communicate without direct references to each other. Each agent gets its own asyncio.Queue when it registers. The bus keeps a full _history of every message sent, useful for debugging and auditing the pipeline.


