from typing import Iterable


class SAME_ITEMS:
    value: Iterable

    def __init__(self, value: Iterable):
        self.value = sorted(value)

    def __eq__(self, value: Iterable):
        return self.value == sorted(value)
