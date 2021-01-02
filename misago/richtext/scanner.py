import re

from mistune.scanner import Scanner


class MisagoScanner(Scanner):
    def __init__(self, rules):
        super().__init__(rules, flags=re.IGNORECASE)
