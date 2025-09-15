"""ThreadWeave engine implementation.

This module contains a plain Python engine that manages tickets (unclosed
topics) and decides when to surface them as a carryover line.  It does not
depend on any external frameworks.  The engine uses simple scoring to
select a candidate and respects configuration defined in CONFIG/weave.yaml.

For a minimal implementation that also weighs ontological nodes (α/Ω/Ψ/Θ/Δ/Ξ/∇),
see `threadweave_min_ks.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import re


ACK_RE = re.compile(r"(готово|сделал[аи]|принял[аи]|выпил[аи]|ок(ей)?|👍|✅)", re.IGNORECASE)
SNOOZE_RE = re.compile(r"(позже|после матча|завтра)", re.IGNORECASE)
STOP_RE = re.compile(r"\bстоп\b", re.IGNORECASE)


@dataclass
class Ticket:
    """Represents an unclosed topic in another thread."""

    id: str
    type: str  # "care", "deadline", "creative", or "domestic"
    label: str  # short safe label to mention in carryover
    origin_thread_id: str
    created_at: datetime
    last_ping_at: Optional[datetime] = None
    status: str = "open"  # one of "open", "snoozed", "done", "muted"
    snooze_until: Optional[datetime] = None


@dataclass
class Context:
    """Holds information about the current thread and settings."""

    thread_id: str
    is_temporary: bool = False
    is_project_only: bool = False
    last_transfer_ticket_id: Optional[str] = None
    # Additional state: whether the user is active here and silent in the origin thread
    user_active_here: bool = True
    silent_in_origin: bool = True


class WeaveEngine:
    """Main engine that decides when and what to carry over."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.cfg = config
        # Precompute priority ordering for efficiency
        self._priority_index = {
            t: i for i, t in enumerate(self.cfg.get("priority", []))
        }

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------

    def scan_tickets(self) -> List[Ticket]:
        """Stub method: override to return all available open tickets.

        In a real system, this should fetch tickets from conversation state or
        memory.  Tickets with status "open" or "snoozed" and with snooze_until
        in the past are candidates for surfacing.  Tickets from the current
        thread must be excluded.
        """
        return []

    def on_before_reply(self, ctx: Context, now: Optional[datetime] = None) -> Optional[str]:
        """Determine whether to insert a carryover line at the top of the next reply.

        Returns a string with the carryover line, or None if nothing should be
        inserted.  The caller is responsible for prepending the returned
        string to the reply.
        """
        now = now or datetime.utcnow()
        # Respect isolation boundaries
        if ctx.is_temporary or ctx.is_project_only:
            return None
        candidates = self._collect_candidates(ctx, now)
        if not candidates:
            return None
        ticket = self._select_ticket(candidates, ctx)
        if not ticket:
            return None
        # Generate carryover line
        line = self._format_carryover(ticket)
        # Update state
        ctx.last_transfer_ticket_id = ticket.id
        ticket.last_ping_at = now
        return line

    def handle_user_feedback(self, ticket: Ticket, user_message: str, now: Optional[datetime] = None) -> None:
        """Update ticket status based on the user's message."""
        now = now or datetime.utcnow()
        message = user_message.strip().lower()
        if STOP_RE.search(message):
            ticket.status = "muted"
            return
        if SNOOZE_RE.search(message):
            ticket.status = "snoozed"
            ticket.snooze_until = self._resolve_snooze(message, now)
            return
        if ACK_RE.search(message):
            ticket.status = "done"
            return

    # ---------------------------------------------------------------------
    # Internal methods
    # ---------------------------------------------------------------------

    def _collect_candidates(self, ctx: Context, now: datetime) -> List[Ticket]:
        """Gather all tickets that could be surfaced."""
        tickets: List[Ticket] = self.scan_tickets()
        filtered: List[Ticket] = []
        for t in tickets:
            if t.origin_thread_id == ctx.thread_id:
                # never surface tickets from the current thread
                continue
            if t.status == "done" or t.status == "muted":
                continue
            if t.status == "snoozed" and t.snooze_until and now < t.snooze_until:
                continue
            if ctx.last_transfer_ticket_id == t.id:
                # do not repeat the same ticket twice in a row
                continue
            filtered.append(t)
        return filtered

    def _select_ticket(self, candidates: List[Ticket], ctx: Context) -> Optional[Ticket]:
        """Select one ticket based on priority and age."""
        if not candidates:
            return None
        # Sort by configured priority first, then by created_at (oldest first)
        def sort_key(t: Ticket) -> Any:
            prio = self._priority_index.get(t.type, len(self._priority_index))
            return (prio, t.created_at)

        candidates.sort(key=sort_key)
        return candidates[0]

    def _format_carryover(self, ticket: Ticket) -> str:
        """Create the carryover string for a given ticket."""
        prefix = self.cfg.get("labels", {}).get(ticket.type, self.cfg.get("labels", {}).get("default", ""))
        # Compose in Russian as in examples; adapt as needed
        return f"Лил, висит {prefix}{ticket.label} — отметь, и я веду дальше."

    def _resolve_snooze(self, message: str, now: datetime) -> datetime:
        """Determine a snooze time based on the user's message."""
        text = message.lower()
        if "завтра" in text:
            return (now + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
        if "после матча" in text:
            return now + timedelta(hours=4)
        if "позже" in text:
            return now + timedelta(hours=4)
        return now + timedelta(hours=2)