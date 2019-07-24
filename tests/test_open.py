import os
import unittest

from bom_open import bom_open

_tests_base = os.path.dirname(__file__)

def _get_test_filename(name):
    return os.path.join(_tests_base, name)


class TestBomOpen(unittest.TestCase):

    def test_utf8le(self):
        with bom_open(_get_test_filename('bom8-sig.txt')) as f:
            self.assertEqual(f.encoding, 'UTF-8-SIG')
            contents = f.read()
        self.assertEqual(contents, 'hello\n')

    def test_utf16le(self):
        with bom_open(_get_test_filename('bom16le.txt')) as f:
            self.assertEqual(f.encoding, 'UTF-16')
            contents = f.read()
        self.assertEqual(contents, 'hello\n')

    def test_utf16be(self):
        with bom_open(_get_test_filename('bom16be.txt')) as f:
            self.assertEqual(f.encoding, 'UTF-16')
            contents = f.read()
        self.assertEqual(contents, 'hello\n')

    def test_empty(self):
        with bom_open(_get_test_filename('empty.txt')) as f:
            self.assertEqual(f.encoding, 'UTF-8')
            contents = f.read()
        self.assertEqual(contents, '')

    def test_invalid(self):
        with bom_open(_get_test_filename('invalid.txt')) as f:
            self.assertEqual(f.encoding, 'UTF-8')
            contents = f.read()
        self.assertEqual(contents, 'Ã(')

    def test_xff(self):
        with bom_open(_get_test_filename('xff.txt')) as f:
            self.assertEqual(f.encoding, 'ISO-8859-1')
            contents = f.read()
        self.assertEqual(contents, '\xff')

    def test_ascii(self):
        with bom_open(_get_test_filename('abc.txt')) as f:
            self.assertEqual(f.encoding, 'ascii')
            contents = f.read()
        self.assertEqual(contents, 'abc\n')

    def test_hz(self):
        with bom_open(_get_test_filename('hz.txt')) as f:
            self.assertEqual(f.encoding, 'UTF-8')
            contents = f.read()
        self.assertEqual(contents, '己所不欲，勿施於人。')
