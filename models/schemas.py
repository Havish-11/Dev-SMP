from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
    source: Optional[str] = None
    raw: str = ""


class AnalyzedLog(BaseModel):
    entries: list[LogEntry]
    error_count: int
    warning_count: int
    summary: str


class ClassifiedIssue(BaseModel):
    error_type: str
    severity: Severity
    description: str
    affected_entries: list[str]
    frequency: int


class FixSuggestion(BaseModel):
    issue_type: str
    commands: list[str]
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: str = "low"


class ValidationResult(BaseModel):
    fix: FixSuggestion
    is_safe: bool
    warnings: list[str]
    approved: bool


class WorkflowResult(BaseModel):
    error_type: str
    issue: ClassifiedIssue
    suggested_fix: Optional[FixSuggestion]
    validation: Optional[ValidationResult]
    final_status: str  # "success", "needs_review", "failed"
    approved_fixes: list[FixSuggestion] = []
