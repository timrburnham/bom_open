import unittest

from stdio_mgr import stdio_mgr

from bom_open import bom_open, StdIOError

class TestBomStdin(unittest.TestCase):

    def test_encoding_utf8(self):
        with stdio_mgr('\uFEFFhello\n') as (in_, out_, err_):
            with bom_open(None) as f:
                self.assertEqual(f.encoding.lower(), 'utf-8-sig')
                contents = f.read()
            self.assertEqual(contents, 'hello\n')

    def test_encoding_utf8_file_dash(self):
        with stdio_mgr('\uFEFFhello\n') as (in_, out_, err_):
            with bom_open('-') as f:
                self.assertEqual(f.encoding.lower(), 'utf-8-sig')
                contents = f.read()
            self.assertEqual(contents, 'hello\n')

    def test_invalid_mode(self):
        with stdio_mgr('\uFEFFhello\n') as (in_, out_, err_):
            with self.assertRaises(StdIOError):
                with bom_open(None, 'w+') as f:
                    self.assertEqual(f.encoding.lower(), 'utf-8-sig')
