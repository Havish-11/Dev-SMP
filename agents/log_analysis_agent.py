import json
from .base_agent import BaseAgent
from models.schemas import LogEntry, AnalyzedLog


class LogAnalysisAgent(BaseAgent):
    """Parses raw log text and extracts structured log entries."""

    def __init__(self):
        super().__init__("log_analysis_agent")

    def analyze(self, raw_logs: str) -> AnalyzedLog:
        system = (
            "You are a log analysis expert. Given raw log text, extract structured "
            "log entries and return ONLY valid JSON — no markdown, no explanation.\n\n"
            "Return this exact schema:\n"
            "{\n"
            '  "entries": [\n'
            '    {"timestamp": "...", "level": "ERROR|WARN|INFO|DEBUG", '
            '"message": "...", "source": "...", "raw": "..."}\n'
            "  ],\n"
            '  "error_count": <int>,\n'
            '  "warning_count": <int>,\n'
            '  "summary": "<one-sentence summary>"\n'
            "}"
        )
        data = self._chat_json(system, f"Analyze these logs:\n\n{raw_logs}")
        entries = [LogEntry(**e) for e in data.get("entries", [])]
        return AnalyzedLog(
            entries=entries,
            error_count=data.get("error_count", 0),
            warning_count=data.get("warning_count", 0),
            summary=data.get("summary", ""),
        )
