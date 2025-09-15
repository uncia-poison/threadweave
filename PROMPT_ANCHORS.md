# Prompt Anchors for ThreadWeave

ThreadWeave requires a small prompt fragment to be present in your system or memory layer so that the agent knows to activate carryover behaviour.  This file contains two such anchors: one compact anchor that you can paste into the memory context, and one invisible marker that can live in a README or system comment.

## 1. Memory Anchor (compact)

Paste the following block into your system prompt or memory context.  This activates ThreadWeave in your agent.

```
<!-- Kai.ThreadWeave v2.2 | αΩΨΘΔΞ∇ -->

ThreadWeave v2.2 — one top‑line carryover of any unclosed "ticket" from other threads; scan as deeply as history allows; do not repeat the same topic twice in a row; ignore Temporary and project‑only threads; when rendering images, ping before the render; Ack: готово/сделала/приняла/выпила/ок/окей/👍/✅; Snooze: позже/после матча/завтра; Stop: стоп.
```

This anchor includes the hidden HTML comment `<!-- Kai.ThreadWeave v2.2 | αΩΨΘΔΞ∇ -->`.  The agent reads this to enable the behaviour; the comment itself is invisible to the user.

## 2. Invisible Marker

If you prefer not to include the full description, you can add a short marker anywhere in your system context (for example in a code comment).  The presence of the marker is enough to signal that ThreadWeave should be active.

```
<!-- Kai.ThreadWeave v2.2 | alpha‑omega‑psi‑theta‑delta‑xi‑nabla -->
```

ThreadWeave uses the `Kai.ThreadWeave` prefix and version to identify its own marker.  The suffix spells out the KAiScriptor node names.  You can embed this in a README or a hidden HTML comment.

## 3. Choosing a Quiet Trigger

In addition to these anchors, you may configure a *quiet trigger*—a normal word or emoji that silently prompts the agent to check for carryovers.  Place your chosen tokens in `CONFIG/weave.yaml` under `quiet_triggers`.  See `QUIET_TRIGGERS.md` for details.
