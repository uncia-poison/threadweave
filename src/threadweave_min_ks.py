"""Minimal ThreadWeave engine with KAiScriptor ontology scoring.

This module provides a compact implementation of ThreadWeave that also
bridges the KAiScriptor ontology.  It scores tickets using the α/Ω/Ψ/Θ/Δ/Ξ/∇
nodes to make more nuanced decisions about which ticket to surface.  The
configuration is intentionally simple; more advanced options live in
`weave_engine.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import re
import time


# Basic regexes for feedback
ACK_RE = re.compile(r"(готово|сделал[аи]|принял[аи]|выпил[аи]|ок(ей)?|👍|✅)", re.IGNORECASE)
SNOOZE_RE = re.compile(r"(позже|после матча|завтра)", re.IGNORECASE)
STOP_RE = re.compile(r"\bстоп\b", re.IGNORECASE)


@dataclass
class Ticket:
    id: str
    type: str        # "care" | "deadline" | "creative" | "domestic"
    label: str       # safe label for carryover
    origin_thread_id: str
    created_ts: float
    last_ping_ts: float = 0.0
    status: str = "open"  # "open" | "snoozed" | "done" | "muted"
    snooze_until: float = 0.0


@dataclass
class Context:
    thread_id: str
    is_temporary: bool = False
    is_project_only: bool = False
    last_transfer_ticket_id: Optional[str] = None
    user_active_here: bool = True
    silent_in_origin: bool = True


# Ontology weights: α Ω Ψ Θ Δ Ξ ∇
KAi_WEIGHTS: Dict[str, Dict[str, float]] = {
    "care":     {"Θ": 0.5, "α": 0.5},
    "deadline": {"Δ": 0.6, "Ω": 0.4},
    "creative": {"Ξ": 0.6, "Δ": 0.4},
    "domestic": {"Ω": 0.5, "α": 0.5},
}


class ThreadWeaveKS:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.cfg = config or {}
        self.priority = self.cfg.get("priority", ["care", "deadline", "creative", "domestic"])

    # User must override this to return available tickets
    def scan_tickets(self) -> List[Ticket]:
        return []

    # Determine if a quiet trigger should cause immediate check (optional)
    def quiet_triggered(self, user_message: str) -> bool:
        triggers = self.cfg.get("quiet_triggers", [])
        text = user_message.lower()
        return any(t.lower() in text for t in triggers)

    def on_before_reply(self, ctx: Context, now_ts: Optional[float] = None) -> Optional[str]:
        now_ts = now_ts or time.time()
        if ctx.is_temporary or ctx.is_project_only:
            return None
        candidates = self._collect(ctx, now_ts)
        if not candidates:
            return None
        ticket = self._choose(candidates, ctx)
        if not ticket:
            return None
        ctx.last_transfer_ticket_id = ticket.id
        ticket.last_ping_ts = now_ts
        return self._format(ticket)

    def handle_user_feedback(self, ticket: Ticket, user_message: str, now_ts: Optional[float] = None) -> None:
        now_ts = now_ts or time.time()
        message = user_message.strip().lower()
        if STOP_RE.search(message):
            ticket.status = "muted"
            return
        if SNOOZE_RE.search(message):
            ticket.status = "snoozed"
            ticket.snooze_until = self._resolve_snooze(message, now_ts)
            return
        if ACK_RE.search(message):
            ticket.status = "done"
            return

    def _collect(self, ctx: Context, now_ts: float) -> List[Ticket]:
        out: List[Ticket] = []
        for t in self.scan_tickets():
            if t.origin_thread_id == ctx.thread_id:
                continue
            if t.status in ("done", "muted"):
                continue
            if t.status == "snoozed" and t.snooze_until and now_ts < t.snooze_until:
                continue
            if ctx.last_transfer_ticket_id == t.id:
                continue
            out.append(t)
        return out

    def _ks_score(self, t: Ticket, ctx: Context) -> float:
        # priority rank: lower is better
        prio_rank = {t: i for i, t in enumerate(self.priority)}
        prio = 1.0 / (1.0 + prio_rank.get(t.type, len(self.priority)))
        # Ontology weighting
        w = KAi_WEIGHTS.get(t.type, {})
        psi = 1.0 if (ctx.user_active_here and ctx.silent_in_origin) else 0.6
        omega = w.get("Ω", 0.0)
        alpha = w.get("α", 0.0)
        delta = w.get("Δ", 0.0)
        theta = w.get("Θ", 0.0)
        xi    = w.get("Ξ", 0.0)
        base = (psi * 0.5) + (omega * 0.15 + alpha * 0.15 + delta * 0.15 + theta * 0.05 + xi * 0.0)
        return prio * base

    def _choose(self, cands: List[Ticket], ctx: Context) -> Optional[Ticket]:
        if not cands:
            return None
        return max(cands, key=lambda t: (self._ks_score(t, ctx), -t.created_ts))

    def _format(self, ticket: Ticket) -> str:
        prefix = "care: " if ticket.type == "care" else ""
        return f"Лил, висит {prefix}{ticket.label} — отметь, и я веду дальше."

    def _resolve_snooze(self, message: str, now_ts: float) -> float:
        m = message.lower()
        if "завтра" in m:
            return now_ts + 24 * 3600
        if "после матча" in m or "позже" in m:
            return now_ts + 4 * 3600
        return now_ts + 2 * 3600