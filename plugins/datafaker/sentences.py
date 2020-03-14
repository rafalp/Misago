import os
import random
from typing import List, Optional


SENTENCES_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "sentences.txt"
)


class Sentences:
    _previous: str
    _sentences: List[str]

    def __init__(
        self, *, sentences_file: str = SENTENCES_FILE, max_length: Optional[int] = None
    ):
        self._sentences = []
        self._previous = ""
        self._len = 0

        with open(sentences_file, "r") as f:
            for sentence in [l.strip() for l in f.readlines()]:
                if max_length and len(sentence) > max_length:
                    continue
                self._sentences.append(sentence)

        random.shuffle(self._sentences)

    def get_random_sentence(self) -> str:
        sentence = random.choice(self._sentences)
        while sentence == self._previous:
            sentence = random.choice(self._sentences)

        self._previous = sentence
        return sentence

    def get_random_sentences(self, count: int) -> List[str]:
        sentences = []
        for _ in range(count):
            sentences.append(self.get_random_sentence())
        return sentences
