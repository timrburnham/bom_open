Context manager to open a file or stdin/stdout. Encoding of text-mode input is detected with chardet. Pass additional args/kwargs to `open()`.

## Differences from `open()`
If `file=None` or `file='-'`, open stdin (when reading) or stdout (when writing) instead.

Write Unicode BOM by default. To override, set `encoding='utf-8'` or non-unicode encoding. Python writes BOM for utf-8-sig, utf-16, or utf-32.  BOM is not written if endianness is specified.
