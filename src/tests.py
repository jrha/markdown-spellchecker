import unittest
import enchant
from spellchecker import abspath
from markspelling import MarkSpelling

class TestFuncts(unittest.TestCase):

    def test_abspath(self):
        """
        Check behaviour of abspath function from main script.
        Not portable (tests assume forward-slash as seperator).
        """
        self.assertEqual(abspath('/tmp/absolute'), '/tmp/absolute')
        relative = 'relative'
        self.assertNotEqual(abspath(relative), relative)
        absolute = abspath(relative)
        self.assertTrue(absolute.endswith('/relative'))
        self.assertTrue(absolute.startswith('/'))


    def test_checkline_no_errors(self):
        """Correctly spelt lines should return no errors"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Lots of words that are spelt correctly!', 'filename.txt', False), 0)


    def test_checkline_one_error(self):
        """Test line with a single spelling error"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('One word that is spelt icnorrectly!', 'filename.txt', False), 1)


    def test_checkline_multi_error(self):
        """Test line with a multiple spelling errors"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Lts of wrods thta are splet icnorrectly!', 'filename.txt', False), 5)


    def test_checkline_code_block_good(self):
        """Test line with no spelling errors inside a block of code"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Lots of words that are spelt correctly!', 'filename.txt', True), 0)


    def test_checkline_code_block_mistake(self):
        """Test that spelling errors are ignored inside a block of code"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Lots of wrods that are spelt icnorrectly!', 'filename.txt', True), 0)


    def test_checkline_backtick_good(self):
        """Test that spelling errors are not flagged by inline code snippets"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('This is an example of `code within backticks`', 'filename.txt', False), 0)


    def test_checkline_backtick_mistake(self):
        """Test that spelling errors are ignored within inline code snippets"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('This is a example of `typso niside backtciks`', 'filename.txt', False), 0)
        self.assertEqual(markspell.checkline('Outside `backtciks` speeling is still improtant', 'filename.txt', False), 2)


    def test_checkline_html_good(self):
        """Test that spelling errors are not flagged by inline HTML"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Test some <strong>inline html</strong>', 'filename.txt', False), 0)
        self.assertEqual(markspell.checkline('Check <i>spelling witihn inline html</i>', 'filename.txt', False), 1)


    def test_checkline_html_mistake(self):
        """Test that spelling errors are ignored within inline HTML"""
        pwl = enchant.request_pwl_dict('dict.txt')
        markspell = MarkSpelling(pwl)
        self.assertEqual(markspell.checkline('Ignore <asd>bad tags</fgh>', 'filename.txt', False), 0)
        self.assertEqual(markspell.checkline('Evrething <qwe>esle mattters</rty>', 'filename.txt', False), 3)


if __name__ == '__main__':
    unittest.main()
