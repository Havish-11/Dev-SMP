from .base_agent import BaseAgent
from models.schemas import FixSuggestion, ValidationResult


class ValidationAgent(BaseAgent):
    """Validates whether a suggested fix is safe to apply."""

    def __init__(self):
        super().__init__("validation_agent")

    def validate(self, fix: FixSuggestion) -> ValidationResult:
        system = (
            "You are a security-conscious SRE. Review proposed shell commands for safety. "
            "Flag anything destructive, irreversible, or requiring elevated privileges. "
            "Return ONLY valid JSON — no markdown.\n\n"
            "Schema:\n"
            "{\n"
            '  "is_safe": true|false,\n'
            '  "warnings": ["..."],\n'
            '  "approved": true|false\n'
            "}"
        )
        user = (
            f"Issue type: {fix.issue_type}\n"
            f"Risk level declared: {fix.risk_level}\n"
            f"Confidence: {fix.confidence}\n"
            f"Reasoning: {fix.reasoning}\n\n"
            "Commands to validate:\n"
            + "\n".join(f"  $ {cmd}" for cmd in fix.commands)
        )
        data = self._chat_json(system, user)
        return ValidationResult(
            fix=fix,
            is_safe=bool(data.get("is_safe", False)),
            warnings=data.get("warnings", []),
            approved=bool(data.get("approved", False)),
        )
