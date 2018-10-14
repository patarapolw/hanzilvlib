from hanzilvlib.dictionary import HanziDict, VocabDict, SentenceDict

hanzi_dict = HanziDict()
vocab_dict = VocabDict()
sentence_dict = SentenceDict()


def test_random_hanzi(rep=10):
    for _ in range(rep):
        print(hanzi_dict.random())


def test_random_vocab(rep=10):
    for _ in range(rep):
        print(vocab_dict.random())


def test_random_sentence(rep=10):
    for _ in range(rep):
        print(sentence_dict.random())
