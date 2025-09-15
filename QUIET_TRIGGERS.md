# Quiet Triggers

ThreadWeave can respond to *quiet triggers*: common words or emojis that you already use in conversation.  The idea is to choose a token that feels natural to you so that you never have to think about invoking ThreadWeave.  When that token appears in your message, the agent interprets it as a hidden cue to check for open tickets and insert a carryover if appropriate.

## How It Works

1. **Choose a token.**  Pick a word, phrase, or emoji that you use frequently.  Examples: `kai`, `thanks`, `🙏`.
2. **Configure it.**  Add your token(s) to the `quiet_triggers` list in `CONFIG/weave.yaml`.
3. **Use as normal.**  Continue your conversations as usual.  Whenever your message contains a trigger, ThreadWeave will silently perform a carryover check.  If it finds a ticket, it will insert a carryover line at the top of its next reply.

Because triggers are ordinary words and emojis, other participants will not notice any special incantations.  The agent simply interprets them as cues to weave threads together.

## Example

Suppose you choose `kai` and `🙏` as your triggers.  You might write:

> kai, can you review the latest sketch?

Even though you did not ask about health reminders, the presence of `kai` prompts ThreadWeave to check for open tickets.  If there is a pending care reminder or unfinished creative review, it will lift that into the reply.

## Configuration

Edit the file `CONFIG/weave.yaml` and set the `quiet_triggers` list.  For example:

```yaml
quiet_triggers:
  - "kai"
  - "🙏"
```

Leave the list empty to disable the feature.
