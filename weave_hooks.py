"""Helper functions to connect ThreadWeave to your agent.

This module contains small wrappers and utilities that you can call from
your conversational agent to integrate ThreadWeave.  They handle timing,
context, and quiet trigger detection.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from .weave_engine import WeaveEngine, Context


def on_before_reply(engine: WeaveEngine, ctx: Context) -> Optional[str]:
    """Call this right before generating a reply.

    It returns a carryover line (if any) that you should prepend to the
    agent's reply.  It automatically fills in the current timestamp.
    """
    return engine.on_before_reply(ctx, now=datetime.utcnow())


def _quiet_triggered(engine: WeaveEngine, user_message: str) -> bool:
    """Check whether the user's message contains a quiet trigger."""
    triggers = engine.cfg.get("quiet_triggers", [])
    text = user_message.lower()
    for trig in triggers:
        if trig.lower() in text:
            return True
    return False


def maybe_quiet_trigger_line(engine: WeaveEngine, ctx: Context, user_message: str) -> Optional[str]:
    """Check for a quiet trigger and, if present, run ThreadWeave.

    This should be called when you receive the user's message.  If the
    message contains a quiet trigger, it invokes `on_before_reply` to
    retrieve a carryover line and returns it.  Otherwise it returns None.
    """
    if _quiet_triggered(engine, user_message):
        return on_before_reply(engine, ctx)
    return None