from django import forms


class SQLReplacerForm(forms.Form):
    sql_code = forms.CharField(
        label='SQL код',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите SQL запрос...',
            'rows': 5
        })
    )

    strings_to_replace = forms.CharField(
        label='Строки для замены (каждая строка на новой линии)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите строки которые нужно заменить...',
            'rows': 5
        })
    )

    replacement_strings = forms.CharField(
        label='Строки замены (каждая строка на новой линии)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите строки для замены...',
            'rows': 5
        })
    )