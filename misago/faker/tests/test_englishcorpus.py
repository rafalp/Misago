from django.test import TestCase

from misago.faker.englishcorpus import EnglishCorpus


class EnglishCorpusTests(TestCase):
    def test_corpus_has_length(self):
        """corpus returns length"""
        corpus = EnglishCorpus()
        self.assertTrue(len(corpus))

    def test_corpus_can_be_shuffled(self):
        """corpus returns length"""
        corpus = EnglishCorpus()
        corpus.shuffle()

    def test_shorter_than_100(self):
        """corpus returns phrases shorter than 100"""
        corpus = EnglishCorpus(max_length=100)
        self.assertTrue(len(corpus))

    def test_longer_than_150(self):
        """corpus returns phrases longer than 150"""
        corpus = EnglishCorpus(min_length=100)
        self.assertTrue(len(corpus))

    def test_random_choice(self):
        """corpus random choice renturns non-repeatable choices"""
        corpus = EnglishCorpus()

        choices = [corpus.random_choice() for _ in range(2)]
        self.assertEqual(len(choices), len(set(choices)))

    def test_random_sentences(self):
        """corpus random_sentences returns x random sentences"""
        corpus = EnglishCorpus()
        self.assertEqual(len(corpus.random_sentences(5)), 5)
