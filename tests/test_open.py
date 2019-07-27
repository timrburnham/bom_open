import locale
import os
import unittest

from bom_open import bom_open

_tests_base = os.path.dirname(__file__)
_tests_locale = locale.getpreferredencoding()

def _get_test_filename(name):
    return os.path.join(_tests_base, name)


class TestContextManagerOpenFile(unittest.TestCase):

    def test_utf8sig(self):
        with bom_open(_get_test_filename('bom8-sig.txt')) as f:
            self.assertEqual(f.encoding.lower(), 'utf-8-sig')
            contents = f.read()
        self.assertEqual(contents, 'hello\n')

    def test_utf8(self):
        with bom_open(_get_test_filename('bom8-sig.txt'),
                      encoding='UTF-8') as f:
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

    def test_windows_curly_quotes(self):
        with bom_open(_get_test_filename('windows-curly-quotes.txt')) as f:
            # Often reported as windows-1250, windows-1252, or windows-1258
            self.assertIn('windows-125', f.encoding.lower())
            contents = f.read()
        self.assertEqual(contents, 'Bob’s Burgers')

    def test_windows_curly_quotes_in_utf8sig(self):
        with bom_open(_get_test_filename('bom8-sig-with-windows-curly-quotes.txt')) as f:
            # Often reported as windows-1250, windows-1252, or windows-1258
            self.assertEqual(f.encoding.lower(), 'utf-8-sig')
            with self.assertRaisesRegexp(UnicodeDecodeError,
                                         "codec can't decode byte 0x92 in position 3: invalid start byte"):
                contents = f.read()

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


class TestNormalOpenFile(unittest.TestCase):

    def test_utf8sig(self):
        f = bom_open(_get_test_filename('bom8-sig.txt'))
        self.assertEqual(f.encoding.lower(), 'utf-8-sig')
        contents = f.read()
        self.assertEqual(contents, 'hello\n')
