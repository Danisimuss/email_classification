import re

from mail_content import MailContent


class Classifier:
    categories = ['Черновик', 'Спам', 'Важное', 'Уведомления', 'Работа']
    tag_words = {
        'Черновик': [
            'черновик', 'draft', 'в процессе', 'надо дописать', 'TODO',
            'не отправлено', 'сохранено', 'временное'
        ],

        'Спам': [
            'спам', 'реклама', 'акция', 'скидка', 'выигрыш', 'приз', 
            'бесплатно', 'заработок', 'деньги', 'кредит', 'казино', 
            'лотерея', 'viagra', 'инвестиции', 'биткоин', 'криптовалюта'
        ],

        'Важное': [
            'срочно', 'важно', 'внимание', 'немедленно', 'критично',
            'дедлайн', 'срок', 'обязательно', 'нужно', 'просьба'
        ],

        'Уведомления': [
            'уведомление', 'подтверждение', 'регистрация', 'восстановление',
            'пароль', 'доступ', 'изменение', 'обновление', 'напоминание',
            'оповещение', 'нотификация', 'уведомить'
        ],

        'Работа': [
            'работа', 'проект', 'задача', 'отчёт', 'совещание', 'бриф',
            'документация', 'клиент', 'контракт', 'договор', 'встреча',
            'презентация', 'отчет', 'план', 'дедлайн', 'исполнить'
        ]
    }

    def __get_text_from_file(self, path):
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                text = file.read()
                return text
                
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except PermissionError:
            print("У вас нет прав на доступ к файлу.")
        except ValueError:
            print("Неверный формат данных.")
        except IOError as e:
            print(f"Произошла ошибка ввода-вывода: {e}.")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}.")
        
        return None


    def __get_mail_category(self, mail):
        haystack = mail.subject + '\n' + mail.content
        haystack = haystack.lower()

        result = []
        for category in Classifier.categories:
            matchLevel = 0
            for keyword in  Classifier.tag_words[category]:
                # Ищем точное вхождение слова
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, haystack))
                if matches > 0:
                    # Взвешиваем: точное совпадение дает больше очков
                    matchLevel += matches * 2.0
                
                # Также ищем частичные совпадения
                if keyword in haystack:
                    matchLevel += 0.5
            
            result.append(matchLevel)

        
        #-------
        #  Тут раздать веса разным категориям
        #-------

        max1 = 0
        maxi = -1
        for i in range(len(result)):
            #print(f'{Classifier.categories[i]}: {result[i]}')
            if result[i] > max1:
                max1 = result[i]
                maxi = i

        if max1 == 0:
            return 'Несортированное'
        
        return  Classifier.categories[maxi]



    def handle_mail(self, path):
        text = self.__get_text_from_file(path)
        if not text:
            return 'Ошибка файла'

        mail = MailContent.mail_from_text(text)
        if not mail:
            return 'Ошибка файла'

        return self.__get_mail_category(mail)
        
