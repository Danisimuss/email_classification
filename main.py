import logging
import shutil
import os
import sys

import email_handler
from classifier import Classifier
from data_analysis import analysis

# class Mail:
#     def __init__(self, email_id, email, email_text, sender):
#         self.mail_id = email_id
#         self.email = email
#         self.mail_text = email_text
#         self.sender = sender
#         self.classification = "unknown"
# #   def email_classification(self): будет реализованно позже




# for num in range(1, 101):
#     email = email_handler.email_getter(num)
#     email_sender = email_handler.get_sender(email)
#     email_text = email_handler.get_text_email(email)
#     email = Mail(num, email, email_text, email_sender)




logging.basicConfig(        #настройки для логов, ошибки и информация в файл и терминал
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)

work_dir=''

#Если пользователь не передал путь через Bash, sys.argv будет содержать только 1 элемент (имя программы) 
if len(sys.argv)>1:
    potential_work_dir=sys.argv[1]
    if os.path.isdir(potential_work_dir):
        work_dir=potential_work_dir
        logging.info('Передан путь к обрабатываемой папке')
    else:
        logging.warning("Путь {potential_work_dir} не является папкой или не существует")
        

#Если передан некорректный аргумент через bash или запуск напрямую, запускаем цикл опроса
while not work_dir:
    print("             НЕОБХОДИМ ВВОД ДАННЫХ")
    print('')

    u_input=input("Сударь, введите корректный путь к обрабатываемой папке или введите exit для выхода: ")
    
    if u_input.lower()=='exit':
        logging.info("Выход из программы, введен exit")
        sys.exit(0)

    if os.path.isdir(u_input):
        work_dir=u_input
        logging.info(f"Введен корректный путь {work_dir}")

    else:
        print(f"Ошибка: Путь {u_input} не найден или не папка")


logging.info(f"Запуск программы обработки и перемещения в папке: {work_dir} ")

classifier = Classifier()
keywords_file = "keywords.json"
classifier.load_keywords(keywords_file)

category_stats = {
    'Ошибка файла': 0,
    'Несортированное': 0
}

for category in classifier.categories:
    category_stats[category] = 0


while True:
    try:
        files=os.listdir(work_dir)
    except FileNotFoundError:
        logging.error(f"Ошибка: Обрабатываемая папка по пути {work_dir} не найдена!")
        break
    
    if not files:
        logging.info("Папка пуста. Завершаю работу")
        break

    file=files[0]
    work_path=os.path.join(work_dir,file)  #Собирает абсолютный путь к обрабатываемому файлу вне зависимости от операционной системы
    
    if os.path.isdir(work_path):
        logging.warning(f"Пропущена папка: {file}") #Если нашли папку, пропускаем
        continue

    #||||||||||||
    target_dir="" #здесь получаем путь перемещения после обработки файла

    try:
        target_dir = classifier.handle_mail(work_path)

        if target_dir in category_stats:
            category_stats[target_dir] += 1
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except PermissionError as e:
        print(f"Ошибка: {e}")

    #||||||||||||

    os.makedirs(target_dir, exist_ok=True)

    """
    Если решим, что будем создавать папку на ходу
    os.makedirs(name,exist_ok=True) #Параметр говорит, если папка уже существует не бросай исключение
    """

    target_path=os.path.join(target_dir,file) #Собирает целевой абсолютный путь куда переместить файл вне зависимости от операционной системы

    try:
        shutil.move(work_path,target_path)
        logging.info(f"{file} перемещен в {target_dir}")

    except Exception:
        logging.exception(f"Ошибка при попытке перемещения с файлом {file}: {Exception}")
        break
        
analysis(category_stats)
