from textwrap import indent
from typing import Any, List

from app.core.config import get_settings
from app.services.llm_client import generate_summary


class AuditAgent:
    """
    Final agent in the chain.

    - Takes the orchestration "state" (logs, deletion actions, identity result).
    - Produces:
        * user_summary  -> short explanation for end-user
        * admin_report  -> detailed technical story for admin
    - Uses LLM if enabled; otherwise, falls back to deterministic templates.
    """

    def run(self, state: Any) -> Any:
        settings = get_settings()

        # ----- 1. Prepare raw text blocks from state -----
        logs_text = self._format_logs(state.logs)
        actions_text = self._format_actions(getattr(state, "deletion_actions", []))

        # Basic, always-available fallbacks:
        user_summary_fallback = self._build_user_summary_fallback(state, actions_text)
        admin_report_fallback = self._build_admin_report_fallback(state, logs_text, actions_text)

        used_llm = False

        # ----- 2. Try LLM for user-facing summary -----
        user_summary = None
        if settings.llm_enabled:
            user_prompt = self._build_user_prompt_for_llm(state, logs_text, actions_text)
            user_summary = generate_summary(user_prompt, max_tokens=350)
            if user_summary:
                used_llm = True

        # ----- 3. Try LLM for admin technical report -----
        admin_report = None
        if settings.llm_enabled:
            admin_prompt = self._build_admin_prompt_for_llm(state, logs_text, actions_text)
            admin_report = generate_summary(admin_prompt, max_tokens=900)
            if admin_report:
                used_llm = True

        # ----- 4. Fallbacks if LLM disabled / fails -----
        state.user_summary = (user_summary or user_summary_fallback).strip()
        state.admin_report = (admin_report or admin_report_fallback).strip()

        # ----- 5. Log what we did -----
        if used_llm:
            state.logs.append("AuditAgent: generated user_summary + admin_report using LLM.")
        else:
            state.logs.append("AuditAgent: generated user_summary + admin_report using templates (LLM disabled or failed).")

        return state

    # ----------------- Helpers -----------------

    def _format_logs(self, logs: List[str]) -> str:
        if not logs:
            return "(no logs captured)"
        return "\n".join(f"- {line}" for line in logs)

    def _format_actions(self, actions: List[Any]) -> str:
        if not actions:
            return "No deletion/masking/flagging actions were recorded."
        lines = []
        for a in actions:
            source = getattr(a, "source_name", "?")
            loc    = getattr(a, "location_type", "?")
            action = getattr(a, "action_type", "?")
            status = getattr(a, "status", "?")
            detail = getattr(a, "details", "")
            line = f"[{source}] ({loc}) -> action={action}, status={status}"
            if detail:
                line += f" | {detail}"
            lines.append(line)
        return "\n".join(lines)

    def _build_user_summary_fallback(self, state: Any, actions_text: str) -> str:
        status = getattr(state, "status", "UNKNOWN")
        request_id = getattr(state, "request_id", "?")
        email = getattr(state, "user_email", "?")
        mode = getattr(state, "mode", "simulation")

        base = [
            f"Your deletion request (ID {request_id}) for account {email} has been processed in {mode} mode.",
            f"Overall status: {status}.",
        ]

        if "No deletion/masking/flagging actions" in actions_text:
            base.append(
                "We did not find any records linked to the identifiers you provided, "
                "so no deletion or masking actions were required."
            )
        else:
            base.append(
                "We located references to your data across one or more connected systems, "
                "and simulated the relevant deletion, masking, or flagging actions according to policy."
            )
        base.append(
            "This environment runs in simulation mode for demo purposes, "
            "so no live production data was actually removed."
        )

        return " ".join(base)

    def _build_admin_report_fallback(self, state: Any, logs_text: str, actions_text: str) -> str:
        request_id = getattr(state, "request_id", "?")
        email = getattr(state, "user_email", "?")
        cust = getattr(state, "user_customer_id", None)
        mode = getattr(state, "mode", "simulation")

        header_lines = [
            f"=== Regent Audit Report ===",
            f"Request ID   : {request_id}",
            f"User email   : {email}",
            f"Customer ID  : {cust or '-'}",
            f"Mode         : {mode}",
            "",
            "---- 1. Orchestration Logs ----",
            logs_text,
            "",
            "---- 2. Deletion / Masking / Flagging Actions ----",
            actions_text,
            "",
            "This report was generated using deterministic templates because the LLM backend is disabled or unavailable.",
        ]

        return "\n".join(header_lines)

    def _build_user_prompt_for_llm(self, state: Any, logs_text: str, actions_text: str) -> str:
        request_id = getattr(state, "request_id", "?")
        email = getattr(state, "user_email", "?")
        mode = getattr(state, "mode", "simulation")

        prompt = f"""
You are a helpful data privacy assistant for a GDPR / CCPA "right to be forgotten" product called Regent.

A user has submitted a deletion request. You will get:
- request id
- user's email
- orchestration mode (e.g. simulation)
- internal logs
- a structured list of actions (mask/delete/flag) taken across systems.

You must write a short explanation (3–6 lines) in simple, friendly language for the end user.
Do NOT expose internal table names or system IDs. Focus on what happened and what it means.

Request context:
- Request ID: {request_id}
- User Email: {email}
- Mode: {mode}

Internal logs (for your understanding, do NOT just repeat them verbatim):
{indent(logs_text, '  ')}

Deletion / masking / flagging actions (summarize impact, do NOT list every row):
{indent(actions_text, '  ')}

Now write a concise message to the user in plain English, in 1 short paragraph, explaining:
- that their request was processed in this environment
- whether data was found, and generally what was done
- that this is a simulation (if mode indicates that)
"""
        return prompt.strip()

    def _build_admin_prompt_for_llm(self, state: Any, logs_text: str, actions_text: str) -> str:
        request_id = getattr(state, "request_id", "?")
        email = getattr(state, "user_email", "?")
        cust = getattr(state, "user_customer_id", None)
        mode = getattr(state, "mode", "simulation")

        prompt = f"""
You are generating an internal technical audit report for a GDPR / CCPA data-rights orchestration engine called Regent.

Audience: privacy / security / data engineering team (not end users).
Goal: summarize what the system actually did step by step.

You are given:
- high-level request metadata
- orchestrator logs
- consolidated deletion/masking/flagging actions across systems.

Write a structured report with the following sections:

1. Request Overview
   - user identifiers
   - mode (e.g. simulation/live)
   - high-level outcome

2. Identity & Discovery
   - how the user was matched (email / customer ID / phone)
   - where data was searched (SQL, Mongo, file storage, etc.)
   - anything notable (no match, partial match, multiple profiles, etc.)

3. Actions by System
   - summarize actions by source (e.g. "customer_db", "events", "adls_customer_exports")
   - mention whether actions were simulated or actually executed
   - highlight any failures or retries

4. Policy Notes / Follow-ups
   - any manual review required
   - any gaps (e.g., systems not integrated yet)
   - any recommended operational follow-up.

Be concise but precise. Use bullet points where useful.

Request metadata:
- Request ID: {request_id}
- User Email: {email}
- Customer ID: {cust or '-'}
- Mode: {mode}

Raw logs:
{indent(logs_text, '  ')}

Raw actions:
{indent(actions_text, '  ')}

Now produce the report using the 4-section structure described above.
"""
        return prompt.strip()
