#!/bin/bash


#запуск через терминал в папке с обрабатываемой директорией: ./run.sh <путь к папке>

get_ts() {
    date +"%Y-%m-%d %H:%M:%S"
}
#  Выводим в консоль
echo "=========================================="
echo "ЗАПУСК СКРИПТА: $(get_ts)"
echo "Текущая рабочая директория: $PWD"
echo "=========================================="

#Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 не найден в системе."
    read -r
    exit 1
fi

#Проверка наличия pip
if ! python3 -m pip --version &> /dev/null; then
    echo "Менеджер пакетов pip не найден для Python 3."
    read -r
    exit 1
fi

#Проверка наличия requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "Файл requirements.txt не найден, без него работа программы не гарантирована"
    read -r
    exit 1
fi

echo 'Установка необходимых библиотек...'
python3 -m pip install -r requirements.txt --quiet --disable-pip-version-check

if [ $? -ne 0 ]; then
    echo 'Ошибка при установке библиотек. Проверьте подключение к интернету или файл requirements.txt'
    read -r
    exit 1
fi

# Запускаем скрипт
python3 main.py "$1" 
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
