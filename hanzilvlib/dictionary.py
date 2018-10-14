import re
import csv
import random
from io import StringIO
import requests
from bs4 import BeautifulSoup
from wordfreq import word_frequency
import json
from cjkradlib import RadicalFinder

try:
    from importlib.resources import read_text as import_text
except ImportError:
    from importlib_resources import read_text as import_text


class HanziDict:
    def __init__(self):
        self.entries = dict()
        reader = csv.DictReader(StringIO(import_text('hanzilvlib.data', 'hanzi_dict.csv')))
        for row in reader:
            self.entries[row['character']] = dict((k, v) for k, v in row.items() if k in {
                'character', 'pinyin', 'meaning', 'heisig', 'kanji'
            })

        self.res = {
            'radical_finder': RadicalFinder(lang='zh'),
            'vocab_dict': VocabDict(),
            'sentence_dict': SentenceDict()
        }

    def search_hanzi(self, hanzi):
        return _HanziObject(self.entries.get(hanzi, {'character': hanzi}), self.res)

    def _random(self):
        return random.choice(tuple(self.entries.values()))

    def random(self):
        return self.search_hanzi(self._random()['character'])


class VocabDict:
    def __init__(self):
        self.entries = dict()
        for i, row in enumerate(import_text('hanzilvlib.data', 'cedict_ts.u8').strip().split('\n')):
            _ = re.match(r'([^ ]+) ([^ ]+) \[(.+)\] /(.+)/', row)
            if _ is not None:
                # trad, simp, pinyin, english = _.groups()
                self.entries[i] = dict(zip(('traditional', 'simplified', 'pinyin', 'english'),
                                                  _.groups()))
            else:
                # print(row)
                pass

        self.res = {
            'sentence_dict': SentenceDict()
        }

    def search_hanzi(self, hanzi, **kwargs):
        def _search():
            for entry in self.entries.values():
                if hanzi in (entry['traditional'] + entry['simplified']):
                    yield _VocabObject(entry, self.res)

        return self.sort_vocab(_search(), **kwargs)

    def search_vocab(self, vocab, **kwargs):
        def _search():
            for entry in self.entries.values():
                if vocab in (entry['traditional'], entry['simplified']):
                    yield _VocabObject(entry, self.res)

        return self.sort_vocab(_search(), **kwargs)

    def search_english(self, english, **kwargs):
        def _search():
            for entry in self.entries.values():
                if english in entry['english']:
                    yield _VocabObject(entry, self.res)

        return self.sort_vocab(_search(), **kwargs)

    @staticmethod
    def sort_vocab(vocab_generator, max_count=10):
        return sorted(vocab_generator, key=lambda entry: -word_frequency(entry['simplified'], 'zh'))[:max_count]

    def _random(self):
        return random.choice(tuple(self.entries.values()))

    def random(self):
        return list(self.search_vocab(self._random()['simplified']))


class SentenceDict:
    def __init__(self):
        self.entries = dict()
        reader = csv.DictReader(StringIO(import_text('hanzilvlib.data', 'SpoonFed.tsv')), delimiter='\t')
        for i, entry in enumerate(reader):
            self.entries[i] = entry

    def _search_sentence(self, vocab):
        for entry in self.entries.values():
            if vocab in entry['sentence']:
                yield _SentenceObject(entry)

    @staticmethod
    def _search_jukuu(vocab):
        params = {
            'q': vocab
        }
        r = requests.get('http://www.jukuu.com/search.php', params=params)
        soup = BeautifulSoup(r.text, 'html.parser')

        for c, e in zip([c.text for c in soup.find_all('tr', {'class': 'c'})],
                        [e.text for e in soup.find_all('tr', {'class': 'e'})]):
            yield _SentenceObject({
                'sentence': c,
                'english': e
            })

    def search_sentence(self, vocab, min_count=10, max_count=10, online=True):
        result = list(self._search_sentence(vocab))

        if len(result) < min_count and online:
            result += list(self._search_jukuu(vocab))

        return result[:max_count]

    def random(self):
        return random.choice(tuple(self.entries.values()))


class _PrintableObject:
    key = NotImplemented
    entry = NotImplemented

    def __getattr__(self, item):
        return self.entry.get(item, None)

    def __getitem__(self, item):
        return getattr(self, item, None)

    def to_json(self):
        return self.entry

    def _repr_pretty_(self, pp, cycle):
        pp.text(json.dumps(self.to_json(), indent=2, ensure_ascii=False, default=repr))

    def __repr__(self):
        return self.key


class _HanziObject(_PrintableObject):
    def __init__(self, entry, res):
        self.res = res
        self.cache = dict()
        self.entry = entry
        self.key = entry['character']

    @property
    def _rad_result(self):
        return self.cache.setdefault('rad_result', self.res['radical_finder'].search(self.key))

    @property
    def compositions(self):
        return self._rad_result.compositions

    @property
    def supercompositions(self):
        return self._rad_result.supercompositions

    @property
    def variants(self):
        return self._rad_result.variants

    @property
    def vocabs(self):
        return self.cache.setdefault('vocabs', self.res['vocab_dict'].search_hanzi(self.key))

    @property
    def sentences(self):
        return self.cache.setdefault('sentences', self.res['sentence_dict'].search_sentence(self.key))

    def to_json(self):
        result = self.entry.copy()
        result.update({
            'compositions': self.compositions,
            'supercompositions': self.supercompositions,
            'variants': self.variants,
            'vocabs': self.vocabs,
            'sentences': self.sentences
        })

        return result


class _VocabObject(_PrintableObject):
    def __init__(self, entry, res):
        self.res = res
        self.cache = dict()
        self.entry = entry
        self.key = entry['simplified']

    @property
    def sentences(self):
        return self.cache.setdefault('sentences', self.res['sentence_dict'].search_sentence(self.key))

    def to_json(self):
        result = self.entry.copy()
        result.update({
            'sentences': self.sentences
        })

        return result


class _SentenceObject(_PrintableObject):
    def __init__(self, entry):
        self.entry = entry
        self.key = entry['sentence']
