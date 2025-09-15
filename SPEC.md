# ThreadWeave Specification (v2.2)

This document defines normative requirements for the ThreadWeave protocol.  The keywords **MUST**, **SHOULD**, and **MUST NOT** have the meanings defined in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

1. **Detection.**  The agent **MUST** detect "hanging tickets" (unclosed topics) as deeply as the conversation history allows.  There is no fixed time window; if the system exposes older context, those tickets are candidates for carryover.

2. **Insertion.**  The agent **MUST** insert exactly one carryover line at the beginning of a reply if a candidate is selected.  The line **SHOULD** avoid revealing private details of the original thread: it uses a concise label describing the ticket (e.g. `care: омега‑3/вода` or `вензеля на колье`).

3. **No Immediate Repeats.**  The agent **MUST NOT** repeat the same ticket in two consecutive agent responses.  After a ticket is mentioned, the next response that includes a carryover **MUST** reference a different ticket, even if the first remains open.

4. **Isolation.**  The agent **MUST** respect isolation boundaries.  Temporary chats and threads marked as project‑only **MUST NOT** receive carryovers.  Tickets originating in such threads are ignored for cross‑thread reminders.

5. **Render Guard.**  If a reply involves generating or editing an image, the agent **MUST** send the carryover ping as a separate message *before* the render.  If sending a separate message is impossible, the carryover **MUST** be deferred to the next text response.

6. **Acknowledgment and Deferral.**  The agent **MUST** interpret any configured acknowledgment word (see `CONFIG/weave.yaml`) as closing the ticket.  Snooze words **MUST** defer it until a later time (the implementation may choose a sensible delay).  Saying `стоп` **MUST** mute carryovers for that ticket until the user re‑enables them.

7. **Selection.**  When multiple tickets are candidates, the agent **SHOULD** select one according to the configured priority: `care` → `deadline` → `creative`/`domestic`.  If there is a tie within a category, the oldest ticket (by creation time) **SHOULD** be chosen.

8. **Quiet Triggers.**  If a quiet trigger is configured and present in the user's message, the agent **SHOULD** treat this as an implicit request to perform carryover selection immediately.  The mechanism for triggers is described in `GUIDE.md` and `QUIET_TRIGGERS.md`.
