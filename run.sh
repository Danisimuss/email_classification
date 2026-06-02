#!/bin/bash

#запуск через терминал в папке с обрабатываемой директорией: ./run.sh <путь к папке>

get_ts() {
    date +"%Y-%m-%d %H:%M:%S"
}

# Конвертация Windows пути в Unix-формат для Git Bash
convert_path() {
    local path="$1"
    # Если путь начинается с буквы диска (C:/, D:/ и т.д.)
    if [[ "$path" =~ ^[A-Za-z]:/ ]]; then
        # Преобразуем C:/Users -> /c/Users
        echo "/${path:0:1}/${path:3}"
    else
        echo "$path"
    fi
}

echo "=========================================="
echo "ЗАПУСК СКРИПТА: $(get_ts)"
echo "Текущая рабочая директория: $PWD"
echo "=========================================="

# Определяем Python (для Windows приоритет у 'python', а не 'python3')
PYTHON_BIN=""
for cmd in python py python3; do
    if command -v "$cmd" >/dev/null 2>&1; then
        # Проверяем, что это действительно Python 3
        VERSION=$("$cmd" -c "import sys; print(sys.version_info[0])" 2>/dev/null)
        if [ "$VERSION" = "3" ]; then
            PYTHON_BIN="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "Python 3 не найден. Убедитесь, что Python 3 установлен и доступен в PATH."
    read -r
    exit 1
fi



echo "Проверка наличия requirements.txt"
#Проверка наличия requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "Файл requirements.txt не найден, без него работа программы не гарантирована"
    read -r
    exit 1
fi

echo 'Установка необходимых библиотек...'
"$PYTHON_BIN" -m pip install -r requirements.txt --quiet --disable-pip-version-check

if [ $? -ne 0 ]; then
    echo 'Ошибка при установке библиотек. Проверьте подключение к интернету или файл requirements.txt'
    read -r
    exit 1
fi

# Запускаем скрипт
"$PYTHON_BIN" main.py "$1"
exit_code=$?

#если есть ошибка в скрипте
if [ $exit_code -ne 0 ]; then
    echo "Python программа завершилась с ошибкой: $exit_code"
    echo "Нажмите Enter, чтобы закрыть окно"
    read -r
    exit $exit_code
fi

echo "=========================================="
echo "РАБОТА СКРИПТА ЗАВЕРШЕНА: $(get_ts)"
echo "=========================================="
echo "Нажмите Enter, чтобы закрыть окно"
read -r
