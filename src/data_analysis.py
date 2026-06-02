import matplotlib.pyplot as plt


def analysis(category_stats):
        #Составляем новый словарь со статистикой без категорий с нулевым счётом
        dct = {}
        for key in category_stats:
                if category_stats[key] > 0:
                        dct[key] = category_stats[key]

        categories = dct.keys()
        plt.figure(figsize=(7, 7))
        plt.pie(dct.values(),
                labels=categories,
                autopct='%1.1f%%',
                startangle=140)
        plt.title('Распределение писем по категориям')
        plt.savefig('email_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
