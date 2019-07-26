import locale
import os
import unittest
import subprocess as sp

from bom_open import bom_open

_tests_base = os.path.dirname(__file__)
_tests_locale = locale.getpreferredencoding()

def _get_test_filename(name):
    return os.path.join(_tests_base, name)

class TestBomOpen(unittest.TestCase):

    def test_utf8le(self):
        with bom_open(_get_test_filename('bom8-sig.txt')) as f:
            self.assertEqual(f.encoding.lower(), 'utf-8-sig')
            contents = f.read()
        self.assertEqual(contents, 'hello\n')

    def test_utf16le(self):
        with bom_open(_get_test_filename('bom16le.txt')) as f:
            self.assertEqual(f.encoding.lower(), 'utf-16')
            contents = f.read()
        self.assertEqual(contents, 'hello\n')

    def test_utf16be(self):
        with bom_open(_get_test_filename('bom16be.txt')) as f:
            self.assertEqual(f.encoding.lower(), 'utf-16')
            contents = f.read()
        self.assertEqual(contents, 'hello\n')

    def test_empty(self):
        with bom_open(_get_test_filename('empty.txt')) as f:
            self.assertEqual(f.encoding, _tests_locale)
            contents = f.read()
        self.assertEqual(contents, '')

    def test_invalid(self):
        with bom_open(_get_test_filename('invalid.txt')) as f:
            self.assertEqual(f.encoding.lower(), 'utf-8')
            contents = f.read()
        self.assertEqual(contents, 'Ã(')

    def test_xff(self):
        with bom_open(_get_test_filename('xff.txt')) as f:
            self.assertEqual(f.encoding.lower(), 'iso-8859-1')
            contents = f.read()
        self.assertEqual(contents, '\xff')

    def test_ascii(self):
        with bom_open(_get_test_filename('abc.txt')) as f:
            self.assertEqual(f.encoding.lower(), 'ascii')
            contents = f.read()
        self.assertEqual(contents, 'abc\n')

    def test_hz(self):
        with bom_open(_get_test_filename('hz.txt')) as f:
            self.assertEqual(f.encoding.lower(), 'utf-8')
            contents = f.read()
        self.assertEqual(contents, '己所不欲，勿施於人。')

    def test_stdin(self):
        pipe = sp.run(['python', _get_test_filename('stdin.py')],
                        input=b'\xff\xfeh\x00i\x00',
                        stdout=sp.PIPE, stderr=sp.PIPE,
                        bufsize=-1)
        encoding = pipe.stderr.decode('utf-8')
        contents = pipe.stdout
        self.assertEqual(encoding.lower(), 'utf-16\n')
        self.assertEqual(contents, b'hi\n')
