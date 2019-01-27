import os
import random

PHRASES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phrases.txt")


class EnglishCorpus:
    def __init__(self, phrases_file=PHRASES_FILE, min_length=None, max_length=None):
        self._countdown = 0
        self._previous = None

        self.phrases = []
        with open(phrases_file, "r") as f:
            for phrase in [l.strip() for l in f.readlines()]:
                if min_length and len(phrase) < min_length:
                    continue
                if max_length and len(phrase) > max_length:
                    continue
                self.phrases.append(phrase)

    def _countdown_to_shuffle(self):
        self._countdown -= 1
        if self._countdown < 0:
            self._countdown = random.randint(500, 1000)
            self.shuffle()

    def __len__(self):
        return len(self.phrases)

    def shuffle(self):
        random.shuffle(self.phrases)

    def random_sentence(self):
        self._countdown_to_shuffle()

        choice = None
        while not choice or choice == self._previous:
            choice = random.choice(self.phrases)

        self._previous = choice
        return choice

    def random_sentences(self, no):
        self._countdown_to_shuffle()

        max_no = len(self) - no - 1
        start = random.randint(0, max_no)

        sentences = self.phrases[start : (start + no)]
        random.shuffle(sentences)

        return sentences
