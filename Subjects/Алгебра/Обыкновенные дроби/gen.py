# Обыкновенные дроби

import pygame
import random
import math
from fractions import Fraction
import os
import sys
path = "Subjects".join(os.getcwd().split("Subjects"))
sys.path.insert(0, path) # изменяем текущую директорию для импорта модулей
from Interface import * # Импортируем: окно с параметрами,
from Convert import convert # конвертер в LaTeX
from Export import export # и окно экспорта

drawer = Drawer("radi(Тип задания, 01, Сложение, Вычитание, Умножение, Деление, Преобразовать, Сложение/Вычитание, Умножение/Деление, Микс); numb(кол-во чисел, 02, 2); numb(кол-во заданий, 03, 1)")

fracs = []
signs = []
sign = [" + ", " - ", " : ", " * "]

def clear_all():
    signs.clear()
    fracs.clear()


def make_fraction(count):
    denominator = random.randint(2, 1 + max(3, 20 // max(1, (count-1))))  # знаменатель
    numerator = random.randint(1, denominator*3)  # числитель
    if count == 1:
        denominator = random.randint(2, 20)  # знаменатель
        numerator = random.randint(denominator, 99)
    if numerator % denominator == 0:
        numerator += 1
    fr = Fraction(numerator, denominator)
    fracs.append(fr)


def replacement(count):
    sum = 0
    for i in range(1, count):
        sum += fracs[i]
    fracs[0] += max(0, math.ceil(sum - fracs[0]))


def solve(count):
    elems = []
    esigns = []
    ress = fracs[0]
    for i in range(1, count):
        if signs[i-1] == " + " or signs[i-1] == " - ":
            elems.append(ress)
            esigns.append(signs[i-1])
            ress = fracs[i]
        elif signs[i-1] == " : ":
            ress = ress / fracs[i]
        elif signs[i-1] == " * ":
            ress = ress * fracs[i]
    elems.append(ress)
    if len(elems) > 0:
        ress = elems[0]
    for i in range(1, len(elems)):
        if esigns[i - 1] == " + ":
            ress += elems[i]
        if esigns[i - 1] == " - ":
            ress -= elems[i]
    #print(elems)
    return ress


def plus(count):
    task = ""
    for i in range(count):
        make_fraction(count)
    ans = Fraction(0, 1)
    for i in range(count):
        ints = math.floor(fracs[i])
        if ints != 0:
            task += str(ints) + " "
        task += str(fracs[i] - ints)
        if i < count - 1:
            task += " + "
            signs.append(" + ")
    ans = solve(count)
    ans_txt = ""
    ints = math.floor(ans)
    if ints != 0:
        ans_txt += str(ints) + " "
    ans_txt += str(ans - ints)
    clear_all()
    return task, ans_txt


def minus(count):
    task = ""
    for i in range(count):
        make_fraction(count)
    fracs.sort(reverse=True)
    replacement(count)
    for i in range(count):
        ints = math.floor(fracs[i])
        if ints != 0:
            task += str(ints) + " "
        task += str(fracs[i] - ints)
        if i < count - 1:
            task += " - "
            signs.append(" - ")
    ans = solve(count)
    ans_txt = ""
    ints = math.floor(ans)
    if ints != 0:
        ans_txt += str(ints) + " "
    ans_txt += str(ans - ints)
    clear_all()
    return task, ans_txt


def multiply(count):
    task = ""
    for i in range(count):
        make_fraction(count)
    for i in range(count):
        ints = math.floor(fracs[i])
        if ints != 0:
            task += str(ints) + " "
        task += str(fracs[i] - ints)
        if i < count - 1:
            task += " * "
            signs.append(" * ")
    ans = solve(count)
    ans_txt = ""
    ints = math.floor(ans)
    if ints != 0:
        ans_txt += str(ints) + " "
    ans_txt += str(ans - ints)
    clear_all()
    return task, ans_txt


def division(count):
    task = ""
    for i in range(count):
        make_fraction(count)
    for i in range(count):
        ints = math.floor(fracs[i])
        if ints != 0:
            task += str(ints) + " "
        task += str(fracs[i] - ints)
        if i < count - 1:
            task += " : "
            signs.append(" : ")
    ans = solve(count)
    ans_txt = ""
    ints = math.floor(ans)
    if ints != 0:
        ans_txt += str(ints) + " "
    ans_txt += str(ans - ints)
    clear_all()
    return task, ans_txt


def converts(count):
    task = ""
    make_fraction(count)
    task += str(fracs[0])
    ans = fracs[0]
    ans_txt = ""
    ints = math.floor(ans)
    if ints != 0:
        ans_txt += str(ints) + " "
    ans_txt += str(ans - ints)
    clear_all()
    return task, ans_txt


def mixed(count, fir, sec):
    task = ""
    for i in range(count):  # генерируем дроби
        make_fraction(count)
    for i in range(count-1):  # генерируем знаки
        signs.append(sign[random.randint(fir, sec)])
    if " - " in signs:
        if " + " in signs:
            el = min(signs.index(" + "), signs.index(" - "))
        else:
            el = signs.index(" - ")
        first = solve(el+1)
        #print(first)
        second = solve(count) - first
        if first + second < 0:
            mid = max(abs(second) // first + 1, abs(first) // second + 1)
            fracs[0] = fracs[0] * mid
    if fracs[0].numerator % fracs[0].denominator == 0:
        fracs[0] += Fraction(1, fracs[0].denominator + 1)
    ans = solve(count)
    for i in range(count):
        ints = math.floor(fracs[i])
        if ints != 0:
            task += str(ints) + " "
        task += str(fracs[i] - ints)
        if i < count - 1:
            task += signs[i]
    #print(ans)
    ans_txt = ""
    ints = math.floor(ans)
    if ints != 0:
        ans_txt += str(ints) + " "
    ans_txt += str(ans - ints)
    clear_all()
    return task, ans_txt


def generate(operation, count=2):
    """
    Функция генерирует квадратные уравнение
    Входных параметров нет
    Вывод: 2 строки - уравнение и ответв формате упрощённой формулы
    Баги: неправильный формат вывода при нулевом корне
    """
    count = int(count)
    #print(count)
    if operation == "Сложение":
        task, ans_txt = plus(count)
    if operation == "Вычитание":
        task, ans_txt = minus(count)
    if operation == "Умножение":
        task, ans_txt = multiply(count)
    if operation == "Деление":
        task, ans_txt = division(count)
    if operation == "Преобразовать":
        task, ans_txt = converts(1)
    if operation == "Сложение/Вычитание":
        task, ans_txt = mixed(count, 0, 1)
    if operation == "Умножение/Деление":
        task, ans_txt = mixed(count, 2, 3)
    if operation == "Микс":
        task, ans_txt = mixed(count, 0, 3)
    return task, ans_txt


# eq, ans = generate()
# print("Уравнение:", eq)
# print("Ответ:", ans)

kg = True  # Условие основного цикла программы


while kg:  # ОЦП (Основной Цикл Программы)
    res = drawer.tick()  # Обновление интерфейса и приём команд пользователя. Для пересоздания интерфейса используется функция reset("новый_ввод")

    # Обработка вывода интерфейса
    if res == 'stop':
        kg = False
    elif res is not None:
        print(res)
        #print("io", res.split(" : ")[2], "io")
        count = res.split("02 : ")[1].split(", 03 ")[0]
        operation = res.split("01 : ")[1].split(", 02 ")[0]
        ktasks = int(res.split("03 : ")[1])
        tasks = ""
        for t in range(ktasks):
            task, answer = generate(operation, count)
            if '/' not in answer and " " in answer:
                answer = answer.split(" ")[0]
            tasks += "Task: " + task + "\n"
            tasks += "Answer: " + answer + "\n"
            #print("task: " + tasks)
            #print("answer: " + answer)
        # print(tasks)
        conv = convert(tasks)
        export(conv)

# & Тут можно складывать, вычитать, умножать, делить и преобразовывать дроби
# & А также можно задавать количество чисел, кроме преобразования

# Выход из программы
pygame.quit()