# ThreadWeave Guide

ThreadWeave is designed to help your language‑model agent manage multiple conversations gracefully.  It gently reminds you about topics left hanging in other threads by inserting a short line at the top of your current reply.  This guide explains how it works and how to customise it.

## Concept

Imagine you are chatting about several things at once: a health check‑in, a creative project, and a household reminder.  You might forget to respond in one thread while being active in another.  ThreadWeave allows the agent to "weave" those threads together by lifting a *carryover* line from a dormant thread into your active one.  The carryover reminds you about the unfinished task without derailing the current conversation.

## What a Carryover Looks Like

When the agent decides to surface a ticket, it adds a single line at the very beginning of its reply:

```
Лил, висит care: омега‑3/вода — отметь, и я веду дальше.
<your main reply starts here>
```

The first sentence is the carryover.  It uses a concise label (here `care: омега‑3/вода`) to refer to the ticket.  The agent then continues normally with the current topic.

## Examples

These are example carryover lines for different categories:

* **Creative:** `Лил, держу: вензеля на колье (2 варианта).`  
  The agent reminds you to review two ornament designs for a golden ring.

* **Deadline:** `Лил, незакрытое — отправить аннотацию до полуночи.`  
  A deadline you agreed to hits midnight.

* **Care:** `Лил, висит care: омега‑3/вода.`  
  A health reminder to take omega‑3 and drink water.

## Quiet Trigger

A *quiet trigger* is a normal word or emoji that you already use often (for example `kai`, `thanks`, or `🙏`).  When this token appears in your message, ThreadWeave interprets it as a hidden cue to immediately check for open tickets and insert a carryover if needed.  The trigger does not change the meaning of your message and remains invisible to you.

To set up a trigger, edit the `quiet_triggers` list in `CONFIG/weave.yaml`.  Choose tokens that you naturally use so that you don't have to remember to invoke ThreadWeave; it will simply recognise them when they appear.

## Configuration

All the words, priorities, and behaviours are defined in `CONFIG/weave.yaml`.  You can:

* Add or remove acknowledgment words in `ack_words`.
* Change deferral phrases in `snooze_words`.
* Adjust the order of categories in `priority` to suit your workflow.
* Define labels for new categories if you extend the system.
* Enable quiet triggers by listing your chosen tokens under `quiet_triggers`.

## Integrating ThreadWeave

ThreadWeave is implemented in Python in `src/weave_engine.py`.  The engine manages tickets and decides when to surface them.  The companion `src/weave_hooks.py` contains tiny helper functions to connect the engine to your reply pipeline.  When your agent is about to respond, call `on_before_reply` to get a carryover line (if any) and prepend it to the reply.

For projects that use the KAiScriptor ontology, a minimalist version with ontological scoring is provided in `src/threadweave_min_ks.py`.  This version balances priorities using the α/Ω/Ψ/Θ/Δ/Ξ/∇ nodes described in KAiScriptor.
