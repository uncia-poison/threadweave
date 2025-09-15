import unittest
from datetime import datetime, timedelta

from threadweave.src.weave_engine import WeaveEngine, Ticket, Context


class TestWeaveEngine(unittest.TestCase):
    def setUp(self) -> None:
        cfg = {
            "priority": ["care", "deadline", "creative", "domestic"],
            "labels": {"care": "care: ", "default": ""},
        }
        self.engine = WeaveEngine(cfg)

    def test_ack_closes_ticket(self) -> None:
        t = Ticket(
            id="1",
            type="care",
            label="омега-3/вода",
            origin_thread_id="A",
            created_at=datetime.utcnow(),
        )
        self.engine.handle_user_feedback(t, "ок ✅")
        self.assertEqual(t.status, "done")

    def test_snooze_sets_future(self) -> None:
        now = datetime.utcnow()
        t = Ticket(
            id="2",
            type="creative",
            label="вензеля на колье",
            origin_thread_id="B",
            created_at=now,
        )
        self.engine.handle_user_feedback(t, "после матча", now)
        self.assertEqual(t.status, "snoozed")
        self.assertIsNotNone(t.snooze_until)

    def test_no_candidates(self) -> None:
        ctx = Context(thread_id="X")
        # No tickets returned; should return None
        line = self.engine.on_before_reply(ctx, datetime.utcnow())
        self.assertIsNone(line)


if __name__ == "__main__":
    unittest.main()
