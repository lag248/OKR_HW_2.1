import sys

from django.test import TestCase
from replacer_app.views import process_string_replacement



class ReplacementLogicTest(TestCase):
    """Тесты логики замены строк"""

    def setUp(self):
        """Выводим информацию перед каждым тестом при -v 2"""
        if '-v' in sys.argv or '--verbose' in sys.argv:
            test_name = self._testMethodName
            print(f"\n--- Запуск теста: {test_name} ---")

    def test_basic_replacement(self):
        """Базовая замена одной строки"""
        sql = 'SELECT * FROM users WHERE email = "old@email.com"'
        old_str = 'old@email.com'
        new_str = 'new@email.com'

        result, error = process_string_replacement(sql, old_str, new_str)

        self.assertIsNone(error)
        self.assertEqual(result, 'SELECT * FROM users WHERE email = "new@email.com"')

    def test_multiple_replacements(self):
        """Замена нескольких строк"""
        sql = 'SELECT name, old_email, old_phone FROM users'
        old_str = 'old_email\nold_phone'
        new_str = 'new_email\nnew_phone'

        result, error = process_string_replacement(sql, old_str, new_str)

        self.assertIsNone(error)
        self.assertIn('new_email', result)
        self.assertIn('new_phone', result)
        self.assertNotIn('old_email', result)
        self.assertNotIn('old_phone', result)

    def test_length_priority(self):
        """Тест приоритета замены самых длинных строк"""
        sql = 'test test123 test12345'
        old_str = 'test\ntest123\ntest12345'
        new_str = 'A\nB\nC'

        result, error = process_string_replacement(sql, old_str, new_str)

        # Самые длинные строки заменяются первыми
        self.assertIsNone(error)
        self.assertEqual(result, 'A B C')

    def test_mismatched_line_count(self):
        """Тест с несовпадающим количеством строк"""
        sql = 'test'
        old_str = 'line1\nline2'
        new_str = 'newline1'

        result, error = process_string_replacement(sql, old_str, new_str)

        self.assertIsNotNone(error)
        self.assertIn('Количество строк', error)
        self.assertIsNone(result)

    def test_empty_strings(self):
        """Тест с пустыми строками"""
        sql = 'SELECT * FROM users'
        old_str = '\n\n'
        new_str = '\n\n'

        result, error = process_string_replacement(sql, old_str, new_str)

        self.assertIsNone(error)
        self.assertEqual(result, sql)

    def test_no_overlap_replacement(self):
        """Тест защиты от повторных замен"""
        sql = 'aaa bbb'
        old_str = 'aaa\nbb'
        new_str = 'bb\naa'

        result, error = process_string_replacement(sql, old_str, new_str)

        self.assertIsNone(error)
        # С учетом логики защиты через временные метки
        self.assertEqual(result, 'bb aab')

    def test_protection_from_double_replacement(self):
        """Тест что уже замененные участки не заменяются повторно"""
        sql = 'test test'
        old_str = 'test\nte'
        new_str = 'replaced\nXX'

        result, error = process_string_replacement(sql, old_str, new_str)

        self.assertIsNone(error)
        # 'test' заменяется на 'replaced'
        # 'te' в 'replaced' НЕ должен заменяться на 'XX' благодаря защите
        self.assertEqual(result, 'replaced replaced')

    def test_special_characters(self):
        """Тест замены строк со специальными символами"""
        sql = 'WHERE path = "/home/user" AND value = "\'test\'"'
        old_str = '/home/user\n\'test\''
        new_str = '/new/path\n"quoted"'

        result, error = process_string_replacement(sql, old_str, new_str)

        self.assertIsNone(error)
        self.assertIn('/new/path', result)
        self.assertIn('"quoted"', result)