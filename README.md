[![Build Status](https://travis-ci.org/timrburnham/bom_open.svg?branch=master)](https://travis-ci.org/timrburnham/bom_open) [![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

Python 3 context manager to open a file or stdio. When reading in text mode, encoding can be detected with chardet. When reading Unicode, always chooses an encoding which removes Byte Order Mark (utf-8-sig, utf-16 or utf-32).

Additional arguments are passed to `open()`.

Python writes a Byte Order Mark for utf-8-sig, utf-16, or utf-32.  Python does not write BOM when endianness is specified.

Differences from `open()`
-------------------------
If `file=None` or `'-'`, open stdin (when reading) or stdout (when writing).

If `encoding=None` and `mode` is readable and text mode ('r' or 'w+'),
file encoding will be detected using chardet.
