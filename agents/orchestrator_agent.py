from .base_agent import BaseAgent
from .log_analysis_agent import LogAnalysisAgent
from .issue_classification_agent import IssueClassificationAgent
from .fix_suggestion_agent import FixSuggestionAgent
from .validation_agent import ValidationAgent
from models.schemas import WorkflowResult


class OrchestratorAgent(BaseAgent):
    """Drives the full log-analysis pipeline end to end."""

    def __init__(self):
        super().__init__("orchestrator_agent")
        self.log_agent = LogAnalysisAgent()
        self.classifier = IssueClassificationAgent()
        self.fixer = FixSuggestionAgent()
        self.validator = ValidationAgent()

    def run(self, raw_logs: str) -> dict[str, WorkflowResult]:
        # Step 1 — parse logs
        analyzed = self.log_agent.analyze(raw_logs)

        # Step 2 — classify issues
        issues = self.classifier.classify(analyzed)

        results: dict[str, WorkflowResult] = {}

        for issue in issues:
            # Step 3 — suggest fix
            fix = self.fixer.suggest(issue)

            # Step 4 — validate fix
            validation = self.validator.validate(fix)

            approved_fixes = [fix] if validation.approved else []

            final_status = (
                "success" if validation.approved
                else "needs_review" if validation.is_safe
                else "failed"
            )

            results[issue.error_type] = WorkflowResult(
                error_type=issue.error_type,
                issue=issue,
                suggested_fix=fix,
                validation=validation,
                final_status=final_status,
                approved_fixes=approved_fixes,
            )

        return results
