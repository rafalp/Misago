from typing import Iterable


class UNORDERED:
    value: Iterable

    def __init__(self, values: Iterable):
        self.value = sorted(values)

    def __eq__(self, value: Iterable):
        return self.value == sorted(value)
