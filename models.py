from math import exp
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Pair:
    anchor: str
    response: str
    user_id: int
    correct: Decimal
    incorrect: Decimal

    def sigmoid(self, x):
        return 1.0 / (1 + exp(-x))

    @property
    def score(self):
        return self.sigmoid(self.incorrect - self.correct)
