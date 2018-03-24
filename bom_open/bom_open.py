import chardet
import codecs
import sys
from io import TextIOWrapper

class StdIOError(Exception):
    pass

class bom_open():
    """Context manager to open a file or stdin/stdout. Encoding of text-mode
    input is detected with chardet. Pass additional args/kwargs to `open()`.

    If `file=None` or `file='-'`, open stdin (when reading) or stdout (when
    writing) instead.

    Write Unicode BOM by default. To override, set `encoding='utf-8'` or
    non-unicode encoding. Python writes BOM for utf-8-sig, utf-16, or utf-32.
    BOM is not written if endianness is specified."""
    def __init__(self,
                 file,
                 mode='r',
                 buffering=-1,
                 encoding='utf-8-sig',
                 *args, **kwargs):
        if file == '-':
            self.file = None
        else:
            self.file = file

        self.mode = mode
        self.buffering = buffering
        self.encoding = encoding
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
            # chardet bytes buffer without advancing file position
            peek = self._f.buffer.peek()
            detect = chardet.detect(peek)
            self.encoding = detect['encoding'] or self.encoding

            # re-attach file with detected encoding
            if self._f.encoding.lower() != self.encoding.lower():
                self._f = TextIOWrapper(self._f.detach(),
                                        encoding=self.encoding)

        return self._f

    def __exit__(self, type, value, traceback):
        self._f.close()
