import re
import os
import pymorphy3
import json
import logging
from transliterate import translit 

logger = logging.getLogger(__name__)

class Classifier:

    def __lemm_one_word(self, word):
        try:
            normal = self.lemmatizer.parse(word)[0].normal_form
            return normal
        except:
            return word


    def __prepare_text(self, text):
        
        text = text.lower()
        words = re.findall(r'\b[а-яё]+\b|\b[a-z]+\b', text)
        res = []
        for word in words:
            if re.fullmatch(r'[a-z]+',word):
                try:
                    word=translit(word,'ru')
                except Exception:
                    logger.debug("Транслитерация не выполнена, обработка без неё")
                    pass
            res.append(self.__lemm_one_word(word))

        return ' '.join(res)


    def __init__(self):
        self.lemmatizer = pymorphy3.MorphAnalyzer()
        self.categories = []
        self.tag_words = {}
        self.default_keywords()



    def default_keywords(self): #Если удалить, упадут тесты
        self.categories = ['Черновик', 'Спам', 'Важное', 'Уведомления', 'Работа']
        self.tag_words = {
            'Черновик': [
                'черновик', 'todo'
            ],

            'Спам': [
                'спам', 'реклама', 'акция', 'скидка'
            ],

            'Важное': [
                'срочно', 'важно',
            ],

            'Уведомления': [
                'уведомление', 'подтверждение',
            ],

            'Работа': [
                'работа', 'коллега'
            ]
        }


    def load_keywords(self, json_path):
        try:
            if not os.path.exists(json_path):
                raise FileNotFoundError('Файл не существует')
            
            
            with open(json_path, 'r', encoding='utf-8') as file:
                self.tag_words = json.load(file)
            
            if not self.tag_words:
                raise ValueError("Пустой или повреждённый файл json")
            
        
            for category in self.tag_words:
                for i in range(len(self.tag_words[category])):
                    self.tag_words[category][i] = self.__prepare_text(self.tag_words[category][i])
                    #print(self.tag_words[category][i])

            self.categories = list(self.tag_words.keys())
            
        except Exception as e:
            self.default_keywords()
            raise Exception(e)


    def __get_text_from_file(self, path):
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                text = file.read()
                return text
                
        except FileNotFoundError:
            logger.error(f"Файл {path} не найден.")
        except PermissionError:
            logger.error("У вас нет прав на доступ к файлу.")
        except ValueError:
            logger.error("Неверный формат данных.")
        except IOError as e:
            logger.error(f"Произошла ошибка ввода-вывода: {e}.")
        except Exception as e:
            logger.error(f"Произошла непредвиденная ошибка: {e}.")
        
        return None



    def __get_mail_category(self, text):
        haystack = text
        haystack = self.__prepare_text(haystack)
        #print(haystack)

        result = []
        for category in self.categories:
            matchLevel = 0
            for keyword in  self.tag_words[category]:
                # Ищем точное вхождение слова
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, haystack))
                if matches > 0:
                    # Взвешиваем: точное совпадение дает больше очков
                    matchLevel += matches * 2
                
                # Также ищем частичные совпадения
                if keyword in haystack:
                    matchLevel += 1
            
            result.append(matchLevel)

        
        #-------
        #  Тут раздать веса разным категориям
        #-------

        max1 = 0
        maxi = -1
        for i in range(len(result)):
            #print(f'{self.categories[i]}: {result[i]}')
            if result[i] > max1:
                max1 = result[i]
                maxi = i

        if max1 == 0:
            return 'Несортированное'
        
        return  self.categories[maxi]



    def handle_mail(self, path):
        text = self.__get_text_from_file(path)
        if text is None:
            return 'Ошибка файла'
        #if text.strip()=='':
            #return 'Черновик' #если пустой файл черновик

        return self.__get_mail_category(text)
        
