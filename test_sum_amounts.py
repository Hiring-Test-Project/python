import unittest

from sum_amounts import Line, Obligation, Settlement, settle


def ob(obligation_id, amount_due, priority):
    return Obligation(obligation_id, amount_due, priority)


def lines(*pairs):
    return [Line(obligation_id, applied) for obligation_id, applied in pairs]


class SettleTest(unittest.TestCase):
    def assert_settlement(self, payment, obligations, unapplied, applied):
        self.assertEqual(Settlement(applied, unapplied), settle(payment, obligations))

    def test_empty(self):
        self.assert_settlement(100, [], 100, [])

    def test_pays_in_full(self):
        self.assert_settlement(
            500,
            [ob(1, 100, 1), ob(2, 40, 3), ob(3, 60, 2)],
            300,
            lines((1, 100), (2, 40), (3, 60)),
        )

    def test_higher_priority_is_paid_first(self):
        self.assert_settlement(
            60,
            [ob(1, 80, 1), ob(2, 50, 9), ob(3, 25, 9)],
            0,
            lines((1, 0), (2, 50), (3, 10)),
        )

    def test_same_priority_pays_earlier_input_first(self):
        self.assert_settlement(
            10,
            [ob(1, 50, 1), ob(2, 30, 1), ob(3, 20, 1)],
            0,
            lines((1, 10), (2, 0), (3, 0)),
        )

    def test_remainder_spills_to_the_next_priority(self):
        self.assert_settlement(
            120,
            [ob(1, 100, 1), ob(2, 40, 5), ob(3, 60, 5)],
            0,
            lines((1, 20), (2, 40), (3, 60)),
        )

    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            settle(5, [ob(1, 10, 1), ob(1, 4, 2)])


if __name__ == "__main__":
    unittest.main()
