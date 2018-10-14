import re
import csv
import random
from io import StringIO

try:
    from importlib.resources import read_text as import_text
except ImportError:
    from importlib_resources import read_text as import_text


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

    def search_hanzi(self, hanzi):
        for entry in self.entries.values():
            if hanzi in (entry['traditional'] + entry['simplified']):
                yield entry

    def search_vocab(self, vocab):
        for entry in self.entries.values():
            if vocab in (entry['traditional'], entry['simplified']):
                yield entry

    def search_english(self, english):
        for entry in self.entries.values():
            if english in entry['english']:
                yield entry

    def random(self):
        """

        :return:
        {'traditional': '廚師長', 'simplified': '厨师长', 'pinyin': 'chu2 shi1 zhang3', 'english': 'executive chef/head chef'}
        {'traditional': '放聲', 'simplified': '放声', 'pinyin': 'fang4 sheng1', 'english': "very loudly/at the top of one's voice"}
        {'traditional': '臺灣白喉噪鶥', 'simplified': '台湾白喉噪鹛', 'pinyin': 'Tai2 wan1 bai2 hou2 zao4 mei2', 'english': '(bird species of China) rufous-crowned laughingthrush (Garrulax ruficeps)'}
        {'traditional': '比利', 'simplified': '比利', 'pinyin': 'Bi3 li4', 'english': 'Pelé (1940-), Edson Arantes Do Nascimento, Brazilian football star'}
        {'traditional': '民生凋敝', 'simplified': '民生凋敝', 'pinyin': 'min2 sheng1 diao1 bi4', 'english': "the people's livelihood is reduced to destitution (idiom); a time of famine and impoverishment"}
        """
        return random.choice(tuple(self.entries.values()))


class HanziDict:
    def __init__(self):
        self.entries = dict()
        reader = csv.DictReader(StringIO(import_text('hanzilvlib.data', 'hanzi_dict.csv')))
        for row in reader:
            self.entries[row['character']] = row

    def search_hanzi(self, hanzi):
        return self.entries.get(hanzi, None)

    def random(self):
        """

        :return:
        OrderedDict([('frequency', '1187'), ('character', '汇'), ('count', '22608'), ('percentile', '91.69936461'), ('pinyin', 'hui4'), ('meaning', 'remit/to converge (of rivers)to exchange, class/collection'), ('heisig', '2673'), ('variant', '匯彙'), ('kanji', 'Variant_WK_L61'), ('vocab', '词汇 詞彙 cí huì vocabulary list of words (e.g. for language teaching purposes) w>汇率 匯率 huì lǜ exchange rate<br>汇报 匯報 huì bào to report to give an account of to collect information and report back<br>')])
        OrderedDict([('frequency', '7720'), ('character', '粏'), ('count', '4'), ('percentile', '99.99789979'), ('pinyin', 'tai4'), ('meaning', ''), ('heisig', '10000'), ('variant', ''), ('kanji', ''), (vocab', '')])
        OrderedDict([('frequency', '9435'), ('character', '篜'), ('count', '1'), ('percentile', '99.99974264'), ('pinyin', 'zheng1'), ('meaning', ''), ('heisig', '10000'), ('variant', ''), ('kanji', ''),('vocab', '篜 篜 zheng1 bamboo<br>')])
        OrderedDict([('frequency', '8808'), ('character', '鑀'), ('count', '2'), ('percentile', '99.99940621'), ('pinyin', 'ai4'), ('meaning', ''), ('heisig', '10000'), ('variant', ''), ('kanji', ''), ('vocab', '鑀 鑀 ai4 einsteinium (chemistry) (Tw)/ionium (former name of thorium)<br>')])
        OrderedDict([('frequency', '7644'), ('character', '馧'), ('count', '5'), ('percentile', '99.99770444'), ('pinyin', 'wo4'), ('meaning', ''), ('heisig', '10000'), ('variant', ''), ('kanji', ''), ('vocab', '')])
        """
        return random.choice(tuple(self.entries.values()))


class SentenceDict:
    def __init__(self):
        self.entries = dict()
        reader = csv.DictReader(StringIO(import_text('hanzilvlib.data', 'SpoonFed.tsv')), delimiter='\t')
        for i, entry in enumerate(reader):
            self.entries[i] = entry

    def get_sentence(self, vocab):
        for entry in self.entries.values():
            if vocab in entry['sentence']:
                yield entry

    def random(self):
        """

        :return:
        OrderedDict([('order', '3142'), ('sentence', '我已经受够了这个计划。'), ('pinyin', 'wǒ yǐjīng shòugòu le zhè gè jìhuà .'), ('english', "I've had enough of this program.")])
        OrderedDict([('order', '5316'), ('sentence', '他拥有公司的很多股份。'), ('pinyin', 'Tā yōngyǒu gōngsī de hěn duō gǔfèn.'), ('english', 'He owns a lot of stock in the company.')])
        OrderedDict([('order', '3103'), ('sentence', '游泳是他唯一的爱好。'), ('pinyin', 'Yóuyǒng shì tā wéiyī de àihào.'), ('english', 'Swimming is his only hobby.')])
        OrderedDict([('order', '7492'), ('sentence', '她把咖啡豆研磨成粉。'), ('pinyin', 'Tā bǎ kāfēidòu yánmó chéng fěn.'), ('english', 'She grinds the coffee beans into powder.')])
        OrderedDict([('order', '7198'), ('sentence', '这片树林很茂密。'), ('pinyin', 'Zhè piàn shùlín hěn màomì.'), ('english', 'This forest is very thick.')])

        """
        return random.choice(tuple(self.entries.values()))
