from Visualiser import *
from Formatter import reformat
from Render import text_to_image
import sys
import pygame
import os

FPS = 30
clock = pygame.time.Clock()
generator = None


def set_generator(subject, theme, gen_name):
    sys.path.insert(0, os.getcwd() + "\\Subjects\\" + subject + "\\" + theme)
    exec("import " + gen_name)
    global generator
    generator = eval(gen_name)


# subject = input("Название предмета: ")
# theme = input("Название темы: ")
# gen_name = input("Файл генератора: ")

subject = "Алгебра"
theme = "Уравнения"
gen_name = "square_equation"

set_generator(subject, theme, gen_name)
if generator is None:
    params_list = "text(Не выбран, 01, генератор)"
else:
    params_list = generator.get_params_list()
drawer = Drawer(params_list)

running = True
while running:  # ОЦП (Основной Цикл Программы)
    res = drawer.tick()  # Обновление интерфейса и приём команд пользователя. Для пересоздания интерфейса используется функция reset("новый_ввод")

    # Обработка вывода интерфейса
    if res == 'stop':
        running = False
    elif res is not None:
        generator.set_params(res["params"])
        tasks = []
        answers = []
        for i in range(res["versions"] * res["tasks"]):
            task, ans = generator.generate()
            print(task)
            print(ans)
            tasks.append(task)
            answers.append(ans)
        text = reformat(tasks, answers, font_size=30, ans_after_each=False, k_versions=res["versions"])
        print(text)
        file_names = text_to_image(text, directory="pages")
        print(file_names)
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
    clock.tick(FPS)

# Выход из программы
# pygame.quit()
try:
    os.remove('pages.txt')
except FileNotFoundError:
    pass
