import codecs
import sys
from io import TextIOWrapper

def bom_detect(bytes_str):
    """Return the Unicode encoding specified by string beginning with
    a Byte Order Mark"""
    encodings = ('utf-8-sig', ('BOM_UTF8',)), \
                ('utf-16', ('BOM_UTF16_LE', 'BOM_UTF16_BE')), \
                ('utf-32', ('BOM_UTF32_LE', 'BOM_UTF32_BE'))

    for enc, boms in encodings:
        for bom in boms:
            magic = getattr(codecs, bom)
            if bytes_str.startswith(magic):
                return enc

    return None

class StdIOError(Exception):
    pass

class bom_open():
    """Context manager to open a file. If reading in text mode and
    Byte Order Mark is present, switch to Unicode encoding specified by BOM.

    If `file=None` or `file='-'`, open stdin (for reading) or stdout (for
    writing) instead.

    Unlike normal `open()`, write BOM by default, even for utf-8. To override,
    set `encoding='utf-8'` or non-unicode encoding."""
    def __init__(self,
                 file,
                 mode='r',
                 buffering=-1,
                 encoding=None,
                 *args, **kwargs):
        if file == '-':
            self.file = None
        else:
            self.file = file
        self.mode = mode
        self.buffering = buffering
        # Python open() writes BOM for utf-8-sig, utf-16, or utf-32
        # BOM is not written if endianness is specified
        self.encoding = encoding or 'utf-8-sig'
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        if self.file:
            self._f = open(self.file,
                           self.mode,
                           self.buffering,
                           self.encoding,
                           *self.args, **self.kwargs)
        elif self.mode == 'r':
            self._f = sys.stdin
        elif self.mode == 'w':
            self._f = sys.stdout
        else:
            raise StdIOError('No file specified, and mode not appropriate '
                             'for stdin (r) or stdout (w)')

        if ('r' in self.mode or '+' in self.mode) and 'b' not in self.mode:
            peek = self._f.buffer.peek()
            detected_encoding = bom_detect(peek)

            self.encoding = detected_encoding or self.encoding

            # re-attach file with new encoding
            if self._f.encoding.lower() != self.encoding.lower():
                self._f = TextIOWrapper(self._f.detach(),
                                        encoding=self.encoding)

        return self._f

    def __exit__(self, type, value, traceback):
        self._f.close()
