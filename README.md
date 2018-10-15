# HanziLvLib

[![PyPI version shields.io](https://img.shields.io/pypi/v/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)
[![PyPI license](https://img.shields.io/pypi/l/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/hanzilvlib.svg)](https://pypi.python.org/pypi/hanzilvlib/)

A library to view contents from [HanziLevelProject](http://hanzilevelproject.blogspot.com/#!), plus some popular dictionaries.

## Features

- Hanzi meanings, variants, [components and supercompositions](https://github.com/patarapolw/cjkradlib), sorted by [Hanzi frequency](http://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO).
- Built-in [CE-DICT](https://www.mdbg.net/chinese/dictionary) and sorted by [vocab frequency](https://pypi.org/project/wordfreq/).
- Sentences from [Chinese Sentences and audio, spoon fed](https://ankiweb.net/shared/info/867291675), and if inadequate, from [Jukuu](http://jukuu.com)

## Installation

```commandline
pip install hanzilvlib
```

## Usage

The contents are contained in two subpackages:-

- `hanzilvlib.dictionary`
- `hanzilvlib.level`

Please see [/example.ipynb](https://github.com/patarapolw/hanzilvlib/blob/master/example.ipynb).

## Related projects

- [HanziLevelUp](https://github.com/patarapolw/HanziLevelUp) - A Hanzi learning suite, with levels based on Hanzi Level Project, aka. another attempt to clone WaniKani.com for Chinese.
- [CJKradlib](https://github.com/patarapolw/cjkradlib) - Generate compositions, supercompositions and variants for a given Hanzi / Kanji
