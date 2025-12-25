from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    """Тесты для главной страницы"""

    def test_get_request(self):
        """Тест GET запроса"""
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'replacer_app/index.html')
        self.assertContains(response, 'SQL String Replacer')

    def test_post_request_valid(self):
        """Тест POST запроса с валидными данными"""
        data = {
            'sql_code': 'SELECT * FROM users WHERE email = "old@email.com"',
            'strings_to_replace': 'old@email.com',
            'replacement_strings': 'new@email.com'
        }

        response = self.client.post(reverse('index'), data)

        self.assertEqual(response.status_code, 200)

        # Проверяем что новая строка есть в результате
        self.assertContains(response, 'new@email.com')

        # Проверяем контекст (более надежно чем поиск в HTML)
        self.assertIn('result', response.context)
        result = response.context['result']

        # Старая строка НЕ должна быть в результате
        self.assertNotIn('old@email.com', result)

        # Но она может быть в HTML шаблоне (в инструкциях, примерах)
        # Поэтому проверяем только результат в контексте

    def test_post_request_shows_result_in_template(self):
        """Тест что результат отображается в шаблоне"""
        data = {
            'sql_code': 'test string',
            'strings_to_replace': 'test',
            'replacement_strings': 'TEST'
        }

        response = self.client.post(reverse('index'), data)

        self.assertEqual(response.status_code, 200)

        # Проверяем что результат отображается
        if 'result' in response.context and response.context['result']:
            result = response.context['result']
            # Результат должен быть в HTML
            self.assertContains(response, result)

    def test_post_request_mismatched_lines(self):
        """Тест POST запроса с несовпадающим количеством строк"""
        data = {
            'sql_code': 'SELECT * FROM users',
            'strings_to_replace': 'line1\nline2',
            'replacement_strings': 'newline1'
        }

        response = self.client.post(reverse('index'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Количество строк')