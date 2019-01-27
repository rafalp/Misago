from ..englishcorpus import EnglishCorpus


def test_corpus_has_length():
    corpus = EnglishCorpus()
    assert corpus


def test_corpus_can_be_shuffled():
    corpus = EnglishCorpus()
    corpus.shuffle()


def test_corpus_can_be_limited_to_phrases_shorter_than_specified():
    corpus = EnglishCorpus(max_length=100)
    assert corpus


def test_corpus_can_be_limited_to_phrases_longer_than_specified():
    corpus = EnglishCorpus(min_length=100)
    assert corpus


def test_corpus_produces_random_sequence():
    corpus = EnglishCorpus()
    choices = [corpus.random_sentence() for _ in range(2)]
    assert len(choices) == len(set(choices))


def test_corpus_produces_list_of_random_sentences():
    corpus = EnglishCorpus()
    assert len(corpus.random_sentences(5)) == 5
