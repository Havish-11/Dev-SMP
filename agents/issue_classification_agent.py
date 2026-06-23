from .base_agent import BaseAgent
from models.schemas import AnalyzedLog, ClassifiedIssue, Severity


class IssueClassificationAgent(BaseAgent):
    """Classifies errors from analyzed logs into structured issues."""

    def __init__(self):
        super().__init__("issue_classification_agent")

    def classify(self, analyzed: AnalyzedLog) -> list[ClassifiedIssue]:
        system = (
            "You are a senior SRE. Classify the errors from analyzed log data into "
            "distinct issue types. Return ONLY a JSON array — no markdown, no explanation.\n\n"
            "Each element:\n"
            "{\n"
            '  "error_type": "...",\n'
            '  "severity": "low|medium|high|critical",\n'
            '  "description": "...",\n'
            '  "affected_entries": ["..."],\n'
            '  "frequency": <int>\n'
            "}"
        )
        user = (
            f"Log summary: {analyzed.summary}\n"
            f"Error count: {analyzed.error_count}, Warning count: {analyzed.warning_count}\n\n"
            "Entries:\n"
            + "\n".join(
                f"[{e.level}] {e.timestamp} — {e.message}" for e in analyzed.entries
            )
        )
        data = self._chat_json(system, user)
        issues = []
        for item in data if isinstance(data, list) else data.get("issues", []):
            try:
                issues.append(ClassifiedIssue(
                    error_type=item["error_type"],
                    severity=Severity(item.get("severity", "medium")),
                    description=item.get("description", ""),
                    affected_entries=item.get("affected_entries", []),
                    frequency=item.get("frequency", 1),
                ))
            except Exception:
                continue
        return issues
