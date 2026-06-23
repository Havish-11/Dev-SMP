from .base_agent import BaseAgent
from models.schemas import ClassifiedIssue, FixSuggestion


class FixSuggestionAgent(BaseAgent):
    """Suggests concrete fix commands for a classified issue."""

    def __init__(self):
        super().__init__("fix_suggestion_agent")

    def suggest(self, issue: ClassifiedIssue) -> FixSuggestion:
        system = (
            "You are a DevOps engineer. Given a classified issue, suggest specific "
            "shell commands to fix it. Return ONLY valid JSON — no markdown, no preamble.\n\n"
            "Schema:\n"
            "{\n"
            '  "issue_type": "...",\n'
            '  "commands": ["cmd1", "cmd2"],\n'
            '  "reasoning": "...",\n'
            '  "confidence": 0.0-1.0,\n'
            '  "risk_level": "low|medium|high"\n'
            "}"
        )
        user = (
            f"Issue type: {issue.error_type}\n"
            f"Severity: {issue.severity.value}\n"
            f"Description: {issue.description}\n"
            f"Frequency: {issue.frequency} occurrences\n"
            f"Affected: {', '.join(issue.affected_entries[:5])}"
        )
        data = self._chat_json(system, user)
        return FixSuggestion(
            issue_type=data.get("issue_type", issue.error_type),
            commands=data.get("commands", []),
            reasoning=data.get("reasoning", ""),
            confidence=float(data.get("confidence", 0.5)),
            risk_level=data.get("risk_level", "low"),
        )
