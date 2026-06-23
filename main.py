"""
Multi-agent log analysis system — powered by Groq.
"""

import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agents import OrchestratorAgent

load_dotenv()
console = Console()

# ---------------------------------------------------------------------------
# Sample logs (replace with real log input as needed)
# ---------------------------------------------------------------------------
SAMPLE_LOGS = """
2024-01-15 10:23:45 ERROR DatabaseConnectionError: Connection refused to postgres://db:5432/prod
2024-01-15 10:23:46 ERROR DatabaseConnectionError: Retry 1/3 failed
2024-01-15 10:23:47 ERROR DatabaseConnectionError: Retry 2/3 failed
2024-01-15 10:23:48 WARN  MemoryUsage: Heap usage at 87% (1.74GB / 2GB)
2024-01-15 10:23:49 ERROR DatabaseConnectionError: Max retries exceeded, giving up
2024-01-15 10:23:50 INFO  RequestHandler: 503 returned to client /api/users
2024-01-15 10:24:01 ERROR NullPointerException in UserService.getProfile() line 142
2024-01-15 10:24:05 WARN  DiskSpace: /var/log partition at 92% capacity
2024-01-15 10:24:10 ERROR SSLHandshakeError: Certificate expired for api.payments.internal
2024-01-15 10:24:15 INFO  HealthCheck: /health returned 200 OK
2024-01-15 10:24:20 ERROR OutOfMemoryError: Java heap space — killing worker process
2024-01-15 10:24:21 WARN  AutoRestart: worker restarted (attempt 3)
"""


def validate_env():
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        console.print(
            "[bold red]Error:[/] GROQ_API_KEY is not set.\n"
            "Get a free key at [link=https://console.groq.com]https://console.groq.com[/link] "
            "then run:\n\n"
            "  export GROQ_API_KEY=your_key_here\n\n"
            "Or create a [bold].env[/] file in this directory:\n\n"
            "  GROQ_API_KEY=your_key_here"
        )
        sys.exit(1)


def get_log_input() -> str:
    """Return logs from a file path arg, stdin pipe, or the built-in sample."""
    if len(sys.argv) > 1:
        path = sys.argv[1]
        with open(path) as f:
            return f.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    console.print("[dim]No log file supplied — using built-in sample logs.[/]\n")
    return SAMPLE_LOGS


def main():
    validate_env()

    raw_logs = get_log_input()

    console.print(Panel(
        "[bold]Multi-Agent Log Analyzer[/]\n[dim]Powered by Groq + LLaMA 3[/]",
        title="🔍 Starting",
    ))

    # ── Step 1: show raw log preview ────────────────────────────────────────
    preview = "\n".join(raw_logs.strip().splitlines()[:8])
    console.print(Panel(f"[dim]{preview}[/]", title="📄 Log Input (preview)"))

    # ── Step 2: run the pipeline ─────────────────────────────────────────────
    console.print("\n[bold cyan]Running agents…[/]\n")
    orchestrator = OrchestratorAgent()

    with console.status("[bold green]Analyzing logs with Groq…[/]"):
        results = orchestrator.run(raw_logs)

    # ── Step 3: print per-issue results ──────────────────────────────────────
    for error_type, r in results.items():
        severity = r.issue.severity.value.upper()
        color = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red", "CRITICAL": "bold red"}.get(severity, "white")

        console.print(Panel(
            f"[{color}]Severity:[/] {severity}\n"
            f"[bold]Description:[/] {r.issue.description}\n"
            f"[bold]Frequency:[/] {r.issue.frequency} occurrence(s)",
            title=f"🐛 {error_type}",
        ))

        if r.suggested_fix:
            fix = r.suggested_fix
            status_icon = "✅" if r.validation and r.validation.approved else "⚠️"
            commands_str = "\n".join(f"  $ {cmd}" for cmd in fix.commands)
            warnings_str = ""
            if r.validation and r.validation.warnings:
                warnings_str = "\n[yellow]Warnings:[/]\n" + "\n".join(
                    f"  • {w}" for w in r.validation.warnings
                )
            console.print(Panel(
                f"{commands_str}\n\n"
                f"[bold]Reasoning:[/] {fix.reasoning}\n"
                f"[bold]Confidence:[/] {fix.confidence:.0%}   "
                f"[bold]Risk:[/] {fix.risk_level}"
                + warnings_str,
                title=f"{status_icon} Suggested Fix",
            ))

    # ── Step 4: summary table ────────────────────────────────────────────────
    table = Table(title="📊 Workflow Summary", show_lines=True)
    table.add_column("Issue Type", style="bold")
    table.add_column("Severity")
    table.add_column("Status")
    table.add_column("Approved Fixes", justify="center")

    for error_type, r in results.items():
        sev = r.issue.severity.value
        status_color = {"success": "green", "needs_review": "yellow", "failed": "red"}.get(
            r.final_status, "white"
        )
        table.add_row(
            error_type,
            sev,
            f"[{status_color}]{r.final_status}[/]",
            str(len(r.approved_fixes)),
        )

    console.print()
    console.print(table)
    console.print("\n[bold green]Done![/]")


if __name__ == "__main__":
    main()
