import json

try:
    from importlib.resources import read_text as import_text
except ImportError:
    from importlib_resources import read_text as import_text


class HanziLevel:
    def __init__(self):
        self.data = json.loads(import_text('hanzilvlib.data', 'level.json'))

    def get_level(self, hanzi):
        for i, hanzi_list in enumerate(self.data['levels']):
            if hanzi in hanzi_list:
                return i

    def get_label(self, hanzi):
        for v in self.data['labels']:
            start, end, label = v
            if hanzi in range(start, end + 1):
                return label

    def get_hanzi_list(self, level):
        return self.data['level'][level]
