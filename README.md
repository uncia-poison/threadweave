# ThreadWeave v2.2 — Cross‑Thread Carryover for LLMs

**ThreadWeave (TW)** is a behavioural method for language‑model agents.  The agent may lift a short top‑line “carryover” in the active thread to remind the user about unfinished topics from other threads (care, deadlines, creative, domestic), without spamming and without questions.  The scanning depth is as deep as the system allows.

## Features

* **Single carryover line.**  A short line appears at the top of the reply, then the agent continues with the current topic.
* **No immediate repeats.**  The same topic is never repeated in two consecutive agent messages.
* **Isolation aware.**  Temporary chats and threads marked project‑only are left untouched.
* **Render guard.**  When generating or editing images, the carryover ping is sent as a separate message before the render; if that is impossible, it is added to the next text response.
* **User control.**  Acknowledgment words like `готово`, `сделала`, `приняла`, `выпила`, `ок`, `окей`, `👍`, or `✅` close a ticket.  Words such as `позже`, `после матча`, or `завтра` defer it.  Saying `стоп` mutes reminders until re‑enabled.

## Quick Start

1. Copy the compact anchor in **PROMPT_ANCHORS.md** into your system or memory layer.  This activates ThreadWeave behaviour.
2. Adjust the lists in **CONFIG/weave.yaml** if you need to customise acknowledgment words, snooze words, priorities, or quiet triggers.
3. Integrate the hook from **src/weave_hooks.py** into the point just before replies are generated.  It will inject carryover lines automatically.

## Quiet Triggers

ThreadWeave can respond to a *quiet trigger*: a common word or emoji that the user already uses (for example `kai`, `thanks`, or `🙏`).  When this token appears in a message, the agent treats it as a hidden cue to check for unclosed tickets and insert a carryover if appropriate.  Configure your preferred trigger(s) in `CONFIG/weave.yaml` under `quiet_triggers`.  Because the trigger is a normal word or emoji, the user does not have to think about it—it remains invisible in conversation.

## Repository Layout

This repository contains both a minimalist implementation and a more complete engine:

| Path                          | Description                                                       |
|-------------------------------|-------------------------------------------------------------------|
| `README.md`                   | The file you are reading.  High‑level overview and quick start. |
| `SPEC.md`                     | Normative specification of the ThreadWeave protocol.            |
| `GUIDE.md`                    | Explanatory guide with examples and quiet trigger notes.         |
| `PROMPT_ANCHORS.md`           | Compact anchor to paste into memory plus invisible marker.       |
| `QUIET_TRIGGERS.md`           | Longer explanation of quiet triggers and configuration.          |
| `CONFIG/weave.yaml`           | YAML configuration with words, labels, render guard and triggers. |
| `src/weave_engine.py`         | A full Python engine for ticket management and carryover logic.  |
| `src/weave_hooks.py`          | Tiny helpers to connect the engine to your reply pipeline.        |
| `src/threadweave_min_ks.py`   | Minimal implementation with KAiScriptor ontology bridge.        |
| `tests/test_weave_engine.py`  | Small unit tests demonstrating basic behaviours.                |
| `SECURITY.md`                 | Ethics and privacy guidelines.                                  |
| `LICENSE`                     | MIT license.                                                    |
| `.gitignore`                  | Ignore common local files.                                      |
