import matplotlib.pyplot as plt
def analysis(category_stats):
        categories = ['Черновик', 'Спам', 'Важное', 'Уведомления', 'Работа', "Ошибка файла", "Несортированное"]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        plt.figure(figsize=(7, 7))
        plt.pie(category_stats,
                labels=categories,
                colors=colors,
                autopct='%1.1f%%',
                startangle=140)
        plt.title('Распределение писем по категориям')
        plt.savefig('email_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
