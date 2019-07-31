import chardet
import codecs
import sys
from io import TextIOWrapper

class StdIOError(Exception):
    pass

class bom_open():
    """Context manager to open a file or stdin/stdout. Encoding can be detected
    with chardet. Pass additional arguments to `open()`.
    Python writes BOM for utf-8-sig, utf-16, or utf-32.  BOM is not written
    when endianness is specified.
    If `file=None` or `'-'`, open stdin (for reading) or stdout (for writing).
    If `encoding=None` and `mode='r'` or `'w+'`, file encoding will be detected
    using chardet."""
    def __init__(self, file, mode='r', buffering=-1, encoding=None,
                 *args, **kwargs):
        if file == '-':
            self.file = None
        else:
            self.file = file

        self.mode = mode
        self.buffering = buffering
        self._encoding = encoding
        self.args = args
        self.kwargs = kwargs
        self._f = None

    def __enter__(self):
        if self.file:
            self._f = open(self.file, self.mode, self.buffering, self._encoding,
                           *self.args, **self.kwargs)
        elif self.mode == 'r':
            self._f = sys.stdin
        elif self.mode == 'w':
            if self._encoding:
                sys.stdout = open(sys.stdout.fileno(), 'w',
                                  encoding=self._encoding,
                                  buffering=1)
            self._f = sys.stdout
        else:
            raise StdIOError('No file specified, and mode not appropriate '
                             'for stdin (r) or stdout (w)')

        if (self._encoding is None
            and 'b' not in self.mode
            and ('r' in self.mode or '+' in self.mode)):
            # run chardet on buffer without advancing file position
            peek = self._f.buffer.peek()
            detected = chardet.detect(peek)
            self._encoding = detected['encoding']

            # re-attach file with detected encoding
            if (self._f.encoding.lower() != (self._encoding or '').lower()):
                self._f = TextIOWrapper(self._f.detach(),
                                        encoding=self._encoding)

        return self._f

    def __exit__(self, type, value, traceback):
        self._f.close()

    def __getattr__(self, name):
        if self._f is None:
            self.__enter__()

        return getattr(self._f, name)

    def close(self):
        if self._f is not None:
            self._f.close()
            self._f = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._f is None:
            self.__enter__()

        return next(self._f)
