from string import printable
import json
import re


if __name__ == '__main__':
    d = dict()

    with open('level.txt') as f:
        for row in f:
            row = row.strip()
            if row:
                if all(c in printable for c in row):
                    start, end, label = re.match(r'(\d+)-(\d+) (\S+)', row).groups()
                    d.setdefault('labels', []).append([int(start), int(end), label])
                else:
                    d.setdefault('levels', []).append(row)

    with open('level.json', 'w') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
