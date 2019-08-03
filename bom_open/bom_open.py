import chardet
import sys
from io import TextIOWrapper

class StdIOError(Exception):
    pass

class bom_open():
    """Open a file or stdio. When reading in text mode, encoding can be detected
    with chardet. When reading Unicode, always chooses an encoding which removes
    Byte Order Mark (utf-8-sig, utf-16 or utf-32).

    If `file=None` or `'-'`, open stdin (when reading) or stdout (when writing).

    If `encoding=None` and `mode` is readable and text mode ('r' or 'w+'),
    file encoding will be detected using chardet.

    Additional arguments are passed to `open()`."""
    def __init__(self, file, mode='r', buffering=-1, encoding=None,
                 *args, **kwargs
    ):
        if file == '-':
            self.file = None
        else:
            self.file = file

        self.mode = mode
        self._buffering = buffering
        self._encoding = encoding
        self._args = args
        self._kwargs = kwargs

        # file name provided
        if self.file:
            self._f = open(self.file, self.mode, self._buffering,
                           self._encoding, *self._args, **self._kwargs)
        # trying to read without file, attach to stdin
        elif self.mode == 'r':
            self._f = sys.stdin
        # trying to write without file, attach to stdout
        elif self.mode == 'w':
            if self._encoding:
                self._buffering = 1
                sys.stdout = open(sys.stdout.fileno(), 'w',
                                  buffering=self._buffering,
                                  encoding=self._encoding,
                                  *self._args, **self._kwargs)
            self._f = sys.stdout
        else:
            raise StdIOError('No file specified, and mode not appropriate '
                             'for stdin (r) or stdout (w)')

        # only attempt character detection if user didn't specify encoding
        if (self._encoding is None
        and 'b' not in self.mode
        and ('r' in self.mode or '+' in self.mode)
        ):
            # run chardet on buffer without advancing file position
            peek = self._f.buffer.peek()
            detected = chardet.detect(peek)
            self._encoding = map_encoding(detected['encoding'])

        # when reading utf-8, force BOM removal.
        if (self.mode == 'r' and self._encoding.lower() == 'utf-8'):
            self._encoding = 'utf-8-sig'

        # re-attach file with detected encoding
        if self._f.encoding.lower() != self._encoding:
            self._f = TextIOWrapper(self._f.detach(),
                                    encoding=self._encoding)


    def __enter__(self):
        return self._f

    def __exit__(self, type, value, traceback):
        self._f.close()

    def __getattr__(self, name):
        return getattr(self._f, name)

    def close(self):
        if self._f is not None:
            self._f.close()
            self._f = None

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._f)

def map_encoding(encoding):
    """Replace specific unwanted encodings with compatible alternative."""
    encoding_map = { None    : 'utf-8',
                     ''      : 'utf-8',
                     'ascii' : 'utf-8' }

    lower_encoding = (encoding or '').lower()
    return encoding_map.get(lower_encoding) or lower_encoding