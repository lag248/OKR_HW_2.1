from django.test import TestCase
from replacer_app.forms import SQLReplacerForm


class SQLReplacerFormTest(TestCase):
    """Тесты для формы SQLReplacerForm"""

    def test_form_valid_data(self):
        """Тест валидных данных формы"""
        form_data = {
            'sql_code': 'SELECT * FROM users',
            'strings_to_replace': 'old@email.com',
            'replacement_strings': 'new@email.com'
        }
        form = SQLReplacerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_widget_attrs(self):
        """Тест атрибутов виджетов формы"""
        form = SQLReplacerForm()

        # Проверяем, что поля имеют правильные классы
        self.assertIn('class="form-control"', str(form['sql_code']))
        self.assertIn('rows="5"', str(form['sql_code']))
        self.assertIn('placeholder="Введите SQL запрос..."', str(form['sql_code']))