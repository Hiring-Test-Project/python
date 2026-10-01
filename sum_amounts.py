from typing import NamedTuple


class Obligation(NamedTuple):
    id: int
    amount_due: int
    priority: int


class Line(NamedTuple):
    id: int
    applied: int


class Settlement(NamedTuple):
    lines: list[Line]
    unapplied: int


def settle(payment: int, obligations: list[Obligation]) -> Settlement:
    raise NotImplementedError("settle")
