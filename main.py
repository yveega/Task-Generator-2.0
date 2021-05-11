
from Visualiser import *
from Formatter import reformat
from Render import text_to_image
import sys
import pygame
import os

generator = None


def set_generator(subject, theme, gen_name):  # Импортирует и выбирает активный генератор
    sys.path.insert(0, os.getcwd() + "\\Subjects\\" + subject + "\\" + theme)
    exec("import " + gen_name)
    global generator
    generator = eval(gen_name)


def get_names(subject, theme):  # Возвращает все имена генераторов из указанной темы
    # Имена написаны в файле генератора после #
    names = {}
    for gen in os.listdir("Subjects/" + subject + "/" + theme):
        if gen[0] == "_":
            continue
        with open("Subjects/" + subject + "/" + theme + "/" + gen, "r", encoding='utf-8') as gen_file:
            names[gen_file.readline().strip().split("# ")[1]] = gen[:-3]
    return names


def get_description(subject, theme, gen):  # Возвращает описание указанного генератора
    # описание генератора может находиться на одной или нескольких строчках после названия в файле генератора
    # каждая строчка описания должна начинаться с # &
    with open("Subjects/" + subject + "/" + theme + "/" + gen + ".py", "r", encoding='utf-8') as gen_file:
        gen_file.readline()
        description = ""
        line = gen_file.readline()
        while line[:4] == "# & ":
            description += line.strip().split("# & ")[1] + "<br>"
            line = gen_file.readline()
    return description


# print(get_names("Алгебра", "Уравнения"))
# subject = input("Название предмета: ")
# theme = input("Название темы: ")
# gen_name = input("Файл генератора: ")

# subject = "Алгебра"
# theme = "Уравнения"
# gen_name = "square_equation"

try:  # программа удаляет файл pages.txt чтобы предыдущие нарисованные страницы не отображались
    os.remove(os.getcwd() + '/pages.txt')
except FileNotFoundError:
    pass

# set_generator(subject, theme, gen_name)
if generator is None:
    params_list = "text(Не выбран, 01, генератор)"
else:
    params_list = generator.get_params_list()
subjects = os.listdir("Subjects")
drawer = Drawer(params_list, subjects=subjects)  # Создаётся объект класса интерфейса

running = True
while running:  # ОЦП (Основной Цикл Программы)
    res = drawer.tick()  # Обновление интерфейса и приём команд пользователя. Для пересоздания интерфейса используется функция reset("новый_ввод")

    # Обработка вывода интерфейса
    if res == 'stop':  # выход из программы
        running = False
    if not type(res) == dict:
        pass
    elif res.get("subject", None) is not None:  # когда пользователь выбрал предмет
        # появляется/обновляется выбор темы из этого предмета
        # print("SUBJECT!!!", res["subject"])
        subject = res["subject"]
        drawer.update_versions_panel(themes=os.listdir("Subjects/" + subject))
    elif res.get("theme", None) is not None:  # когда пользователь выбрал тему
        # появляется/обновляется выбор генератора из этой темы
        # print("THEME!!!", res["theme"])
        theme = res["theme"]
        gens = get_names(subject, theme)
        drawer.update_versions_panel(themes=os.listdir("Subjects/" + subject), generators=list(gens.keys()))
    elif res.get("generator", None) is not None:  # когда пользователь выбрал генератор
        # выставляются параметры генерации и описание генератора
        # print("GENERATOR!!!", res["generator"])
        gen_name = res["generator"]
        gens = get_names(subject, theme)
        description = get_description(subject, theme, gens[gen_name])
        set_generator(subject, theme, gens[gen_name])
        drawer.update_params(generator.get_params_list(), description)
        # print(description)
    elif res.get("generate", None) is not None:  # если запущена генерация или перерисовка
        # print(res)
        if res["generate"]:  # проверка нужно ли генерировать задания заново
            generator.set_params(res["gen_params"])
            tasks = []
            answers = []
            for i in range(res["versions"] * res["tasks"]):
                task, ans = generator.generate()
                # print(task)
                # print(ans)
                tasks.append(task)
                answers.append(ans)
        text = reformat(tasks, answers, font_size=res["fontsize"], ans_after_each=False, k_versions=res["versions"],
                        font=res["font"])
        # print(text)
        file_names = text_to_image(text, directory="pages")
        # print(file_names)
        f = open('pages.txt', 'w')
        s = ""
        for name in file_names:
            s += os.getcwd() + "\\pages\\" + name + "\n"
        s = s[:-1]
        # print(s)
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
