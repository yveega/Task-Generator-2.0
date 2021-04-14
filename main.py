from Visualiser import *
from Formatter import reformat
from Render import text_to_image
import square_equation
from random import randint as r
import os

drawer = Drawer(square_equation.get_params_list())

running = True
while running:  # ОЦП (Основной Цикл Программы)
    res = drawer.tick()  # Обновление интерфейса и приём команд пользователя. Для пересоздания интерфейса используется функция reset("новый_ввод")

    # Обработка вывода интерфейса
    if res == 'stop':
        running = False
    elif (res is not None) and (not r(0, 1)):
        square_equation.set_params(res)
        tasks = []
        answers = []
        for i in range(5):
            task, ans = square_equation.generate()
            print(task)
            print(ans)
            tasks.append(task)
            answers.append(ans)
        text = reformat(tasks, answers, font_size=30)
        file_names = text_to_image(text, directory="pages")
        f = open('pages.txt', 'w')
        s = ""
        for name in file_names:
            s += os.getcwd() + "\\pages\\" + name + "\n"
        s = s[:-1]
        print(s)
        # s = r'''C:/Users/ПК/Desktop/проги/проект9.2.2/test_img/latex_A41.png
        # C:/Users/ПК/Desktop/проги/проект9.2.2/test_img/latex_A42.png
        # C:/Users/ПК/Desktop/проги/проект9.2.2/test_img/latex_A43.png'''
        print(s, file=f)
        f.close()

# Выход из программы
# pygame.quit()
try:
    os.remove('pages.txt')
except FileNotFoundError:
    pass
