import pytest
import os
import tempfile
from src.classifier import Classifier


@pytest.fixture
def classifier():
#Cоздаёт классификатор с ключевыми словами из json
    
    clf = Classifier()
    clf.load_keywords("config/keywords.json")  
    return clf


@pytest.fixture
def temp_file():
#Cоздаёт временный файл и удаляет его после теста
    files = []
    def _create(content, ext='.txt'):
        with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False, encoding='utf-8') as f:
            f.write(content)
            files.append(f.name)
        return f.name
    yield _create
    for path in files:
        if os.path.exists(path):
            os.remove(path)


#основные тесты
@pytest.mark.parametrize('text,expected', [
    ('срочно нужно сделать', 'Важное'),
    ('это просто черновик', 'Черновик'),
    ('акция и скидка', 'Спам'),
    ('коллега по работе', 'Работа'),
    ('уведомление о подтверждении', 'Уведомления'),
])

def test_category_match(classifier, temp_file, text, expected):
    path = temp_file(text)
    assert classifier.handle_mail(path) == expected


@pytest.mark.parametrize('text', [ 'абракадабра без ключевых слов',"933979 7268856", 'jbfbbwbvnb'])
def test_no_match_fallback(classifier, temp_file, text):
    path = temp_file(text)
    assert classifier.handle_mail(path) == 'Несортированное'


def test_empty_file(classifier, temp_file):
    path = temp_file('')
    assert classifier.handle_mail(path)=='Черновик' 


def test_unsupported_extension(classifier, temp_file):
#Файл с неизвестным расширением
    path = temp_file('срочно', ext='.xyz')
    result = classifier.handle_mail(path)
    assert isinstance(result, str)  # Возвращает строку, а не исключение


#сложные тесты
@pytest.mark.parametrize('text,expected', [
    ('СРОЧНО! Акция!', 'Спам'),       
    ('черновик срочно', 'Черновик'),  
    ('Тест с Ё и ёжиком', 'Несортированное'),  
    ('todo list', 'Черновик'),         
])

def test_complex_cases(classifier, temp_file, text, expected):
    path = temp_file(text)
    assert classifier.handle_mail(path) == expected


def test_nonexistent_file(classifier):
#несуществующий файл
    assert classifier.handle_mail('/nonexistent/path.txt')=='Ошибка файла'


