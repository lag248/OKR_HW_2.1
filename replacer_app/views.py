from django.shortcuts import render
from .forms import SQLReplacerForm

def process_string_replacement(sql_code, strings_to_replace, replacement_strings):
    """
    Надежная замена с использованием меток для уже замененных участков
    """
    # Разбиваем строки на списки
    old_strings = [s.strip() for s in strings_to_replace.split('\n') if s.strip()]
    new_strings = [s.strip() for s in replacement_strings.split('\n') if s.strip()]

    # Проверяем что количество строк совпадает
    if len(old_strings) != len(new_strings):
        return None, "Количество строк в обоих наборах должно совпадать"

    # Создаем пары для замены и сортируем по убыванию длины старых строк
    replacement_pairs = list(zip(old_strings, new_strings))
    replacement_pairs.sort(key=lambda x: (-len(x[0]), x[0]))  # Длина (убывание), затем сама строка

    # Временные метки для защиты замененных участков
    protected_regions = []
    result = sql_code

    # Сначала заменяем все самые длинные строки и помечаем их
    for i, (old_str, new_str) in enumerate(replacement_pairs):
        if not old_str:
            continue

        # Создаем уникальную метку для этого замененного участка
        placeholder = f"__PROTECTED_{i:08d}__"

        # Заменяем old_str на временную метку
        result = result.replace(old_str, placeholder)

        # Сохраняем информацию о замене
        protected_regions.append((placeholder, new_str))

    # Затем заменяем временные метки на финальные значения
    for placeholder, final_value in protected_regions:
        result = result.replace(placeholder, final_value)

    return result, None

def index(request):
    result = None
    error = None
    original_sql = None

    if request.method == 'POST':
        form = SQLReplacerForm(request.POST)
        if form.is_valid():
            sql_code = form.cleaned_data['sql_code']
            strings_to_replace = form.cleaned_data['strings_to_replace']
            replacement_strings = form.cleaned_data['replacement_strings']

            original_sql = sql_code
            result, error = process_string_replacement(
                sql_code,
                strings_to_replace,
                replacement_strings
            )
    else:
        form = SQLReplacerForm()

    return render(request, 'replacer_app/index.html', {
        'form': form,
        'result': result,
        'error': error,
        'original_sql': original_sql
    })