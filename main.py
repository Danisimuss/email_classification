import logging
import shutil
import os
import sys

from classifier import Classifier




os.makedirs('logs',exist_ok=True)
logging.basicConfig(        #настройки для логов, ошибки и информация в файл и терминал
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

work_dir=''

#Если пользователь не передал путь через Bash, sys.argv будет содержать только 1 элемент (имя программы) 
if len(sys.argv)>1:
    potential_work_dir=sys.argv[1]
    if os.path.isdir(potential_work_dir):
        work_dir=potential_work_dir
        logging.info('Передан путь к обрабатываемой папке')
    else:
        logging.warning(f"Путь {potential_work_dir} не является папкой или не существует")
        

#Если передан некорректный аргумент через bash или запуск напрямую, запускаем цикл опроса
while not work_dir:
    print("             НЕОБХОДИМ ВВОД ДАННЫХ")
    print('')

    u_input=input("Введите корректный путь к обрабатываемой папке или введите exit для выхода: ")
    
    if u_input.lower()=='exit':
        logging.info("Выход из программы, введен exit")
        sys.exit(0)

    if os.path.isdir(u_input):
        work_dir=u_input
        logging.info(f"Введен корректный путь {work_dir}")

    else:
        print(f"Ошибка: Путь {u_input} не найден или не папка")

work_dir=os.path.abspath(work_dir)

logging.info(f"Запуск программы обработки и перемещения в папке: {work_dir} ")

classifier = Classifier()
keywords_file = "keywords.json"
classifier.load_keywords(keywords_file)

SUPPORTED_EXTENSIONS={'.txt'}

try:
    files=os.listdir(work_dir)
except FileNotFoundError:
    logging.error(f"Ошибка: Обрабатываемая папка по пути {work_dir} не найдена!")
    sys.exit(1)

files = [f for f in files if os.path.isfile(os.path.join(work_dir, f))]
if not files:
    logging.info("Папка пуста. Завершаю работу")
    sys.exit(0)

logging.info(f"Найдено {len(files)} фалов для обработки")



for file in files:
    
    work_path=os.path.join(work_dir,file)  #Собирает абсолютный путь к обрабатываемому файлу вне зависимости от операционной системы 
    
    _,ext=os.path.splitext(file.lower())

    if ext not in SUPPORTED_EXTENSIONS:
        target_dir='Неподдерживаемое расширение'
        logging.info(f'Файл {file} имеет неподдерживаемый формат')
    
    else:

        try:
            target_dir = classifier.handle_mail(work_path)

        except Exception as e:
            logging.error(f"Ошибка с файлом {file} :{e}")
            target_dir = 'Несортированное'
        
        if target_dir in ('', None,'Ошибка файла','Несортированное'):
            target_dir='Несортированное'

        #exit(0)
        #continue
    
    os.makedirs(target_dir, exist_ok=True) # создаем папку на ходу
    target_path=os.path.join(target_dir,file) #Собирает целевой абсолютный путь куда переместить файл вне зависимости от операционной системы

    try:
        shutil.move(work_path,target_path)
        logging.info(f"{file} перемещен в {target_dir}")
    except Exception as e:
        logging.exception(f"Ошибка при попытке перемещения с файлом {file}: {e}")
        continue

logging.info("Обработка всех файлов выполнена")