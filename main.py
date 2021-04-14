from Visualiser import *
from random import randint as r
import os

drawer = Drawer("numb(макс. знаменатель корней, 01, 20);" +
                "numb(bs, 0, 100)")

running = True
while running:  # ОЦП (Основной Цикл Программы)
    res = drawer.tick()  # Обновление интерфейса и приём команд пользователя. Для пересоздания интерфейса используется функция reset("новый_ввод")

    # Обработка вывода интерфейса
    if res == 'stop':
        running = False
    elif (res is not None) and (not r(0, 1)):
        f = open('pages.txt', 'w')
        s = os.getcwd() + "\\test_img\\latex_A41.png\n" + os.getcwd() + "\\test_img\\latex_A42.png\n" + os.getcwd() + "\\test_img\\latex_A43.png"
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