from ..sentences import Sentences


def test_sentences_list_instance_returns_random_sentence():
    sentences = Sentences()
    assert sentences.get_random_sentence()


def test_sentences_list_instance_returns_random_sentences():
    sentences = Sentences()
    assert sentences.get_random_sentences(5)


def test_max_len_of_sentence_returned_can_be_specified():
    sentences = Sentences(max_length=10)
    assert len(sentences.get_random_sentence()) <= 10
