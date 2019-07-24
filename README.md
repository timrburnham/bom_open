[![Build Status](https://travis-ci.org/timrburnham/bom_open.svg?branch=master)](https://travis-ci.org/timrburnham/bom_open) [![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

Python 3 context manager to open a file or stdin/stdout. Encoding can be detected with chardet. Pass additional arguments to `open()`.

Python writes Byte Order Mark for utf-8-sig, utf-16, or utf-32.  BOM is not written when endianness is specified.

Differences from `open()`
-------------------------
If `file=None` or `'-'`, open stdin (for reading) or stdout (for writing).

If `encoding=None` and `mode='r'` or `'w+'`, file encoding will be detected using chardet.
