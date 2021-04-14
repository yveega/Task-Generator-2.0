# Квадратные уравнения
# & ax + by + c = d
"""
Модуль, генерирующий задачи по квадратным уравнениям

Использует библиотеки math и random
Используемые: функция generate, get_params_list, set_params
Баги: в случае, если один из корней равен 0, вывод некорректный
Работал над модулем: Агеев Николай
Дата последнего изменения: 12.04.2021
"""
import random
import math
import os
import sys
path = "Subjects".join(os.getcwd().split("Subjects"))
sys.path.insert(0, path)


# Функция возвращает список параметров для этого генератора в виде строки
def get_params_list():
    return "numb(макс. знаменатель корней, 02, 3); numb(вероятность совпадения корней в %, 03, 50)"


# Функция устанавливает параметры генерации задач, принимает строку со словарём
def set_params(params):
    global max_den, p_equal
    max_den, p_equal = params.split(", ")
    max_den = int(max_den.split(" : ")[1])
    p_equal = int(p_equal.split(" : ")[1])


def generate():
    """
    Функция генерирует квадратные уравнение
    Входных параметров нет
    Вывод: 2 строки - уравнение и ответв формате упрощённой формулы
    Баги: неправильный формат вывода при нулевом корне
    """
    # устанавливаем корни
    num_1 = random.randint(-20, 20)
    den_1 = random.randint(1, max_den)
    num_1 //= math.gcd(num_1, den_1)
    den_1 //= math.gcd(num_1, den_1)
    if random.random() < p_equal:
        num_2, den_2 = num_1, den_1
    else:
        num_2 = random.randint(-20, 20)
        den_2 = random.randint(1, max_den)
    num_2 //= math.gcd(num_2, den_2)
    den_2 //= math.gcd(num_2, den_2)
    # форматируем ответ
    ans_1 = "t(" + str(num_1) + ")" if den_1 == 1 else "t(" + str(num_1) + " / " + str(den_1) + ")"
    if num_1 < 0:
        ans_1 = "- " + ans_1[1:]
    ans_2 = "t(" + str(num_2) + ")" if den_2 == 1 else "t(" + str(num_2) + " / " + str(den_2) + ")"
    if num_2 < 0:
        ans_2 = "- " + ans_2[1:]
    if ans_1 != ans_2:
        answer = "C8C(t(x))(i(1)())(t( = ))({})(t(, x))(i(2)())(t( = ))({})".format(ans_1, ans_2)
    else:
        answer = "c(t(x = ))(" + ans_1 + ")"

    # eq_type = random.randint(1, 3)
    eq_type = 1
    if eq_type == 1:
        # считаем коеффициенты
        k_square = den_1 * den_2
        k_simple = -den_1 * num_2 - den_2 * num_1
        k_const = num_1 * num_2
        # форматируем выражение
        if k_square == 1:
            equation = "c(t(x))(i()(2))"
        elif k_square == -1:
            equation = "c(t(- x))(i()(2))"
        else:
            equation = "c(t(" + str(k_square) + " x))(i()(2))"

        if k_simple == 1:
            equation = "c(" + equation + ")(t( + x))"
        elif k_simple == -1:
            equation = "c(" + equation + ")(t(- x))"
        if k_simple > 0:
            equation = "c(" + equation + ")(t(+ " + str(k_simple) + " x ))"
        elif k_simple < 0:
            equation = "c(" + equation + ")(t(- " + str(-k_simple) + " x ))"

        if k_const > 0:
            equation = "c(" + equation + ")(t(+ " + str(k_const) + " = 0))"
        elif k_const < 0:
            equation = "c(" + equation + ")(t(- " + str(-k_const) + " = 0))"
        else:
            equation = "c(" + equation + ")(t(= 0))"
        # возвращаем ответ
        return equation, answer


# set_params("02 : 3, 03 : 50")
# print(generate())
#
# print(generate())
#
# print(generate())
#
# print(generate())
set_params("02 : 3, 03 : 50")
tasks = []
answers = []
for _ in range(6):
    t, a = generate()
    tasks.append(t)
    answers.append(a)
print(tasks)
print(answers)
