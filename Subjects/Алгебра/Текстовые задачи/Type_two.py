# Задачи с процентами
# & Текстовые задачи вида
# & "Найти число, если после нескольких действий оно увеличилось/уменьшилось на Х"

"""
Модуль, генерирующий текстовые задачи

Использует библиотеку random
Используемые: функция generate и decode_output
Баги: процент на одной из стадий может быть равен 0. В этом случае задача значительно упрощается.
Работал над модулем: Кудряшов Илья (основа была взята с модуля Агеева Николая)
Дата последнего изменения: 16.03.2021
"""

from random import randint
from math import ceil
import os
import sys
sys.path.insert(0, os.getcwd().split("Subjects")[0])
os.chdir(os.getcwd().split("Subjects")[0])
print(os.getcwd())
from Interface import *
from Convert import convert
from Export import export_alternative

print("text generation is running...")

task_pattern = """Некоторое число WORD на PROCENT%, после чего результат WORd на PROCENt%.
В конце указанных преобразований число RESULT
в сравнении с начальным. Найдите начальное число."""

def decode_output(out):
    answ = {}
    for part in out.split(','):
        chopped = part
        while len(chopped) > 0 and chopped[0] == ' ':
            chopped = chopped[1:]
        key, value = chopped.split(' : ')
        answ[key] = value
    return answ

def generate(output):
    out = decode_output(output)
    ugly = out['uglynumbs'] == '1'
    uglyperc = out['uglyperc'] == '1'
    maxansw = int(out['maxansw'])
    while True:
        answ = randint(2, maxansw if not ugly else maxansw * 100)
        percs = []
        for i in range(2, 100 if out['bigcent'] == '0' else 300):
            if round(answ * i / 100) == answ * i / 100:
                for j in range(1, 100 if out['bigcent'] == '0' else 300):
                    if round((answ + answ * i / 100) * j / 100) == (answ + answ * i / 100) * j / 100 and (round(j * i / 100) == j * i / 100 or uglyperc) and i % 50 != 0 and j % 50 != 0:
                        percs.append([i, j])
                    if round((answ - answ * i / 100) * j / 100) == (answ - answ * i / 100) * j / 100 and (round(j * i / 100) == j * i / 100 or uglyperc) and i < 100 and j < 100:
                        percs.append([-i, j])
        if len(percs) > 0:
            break
    perc = percs[randint(0, len(percs) - 1)]
    if perc[0] < 0:
        perc[1] *= -1
    if out['idmixer'] == '1' and randint(1, 100) > 30 and out['bigcent'] == '0':
        perc[1] *= -1
    dif = int(answ * (1 + perc[0] / 100) * (1 + perc[1] / 100) - answ)
    if ugly:
        dif /= 100
        answ /= 100
    answer = task_pattern
    answer = answer.replace('WORD', 'уменьшили' if perc[0] < 0 else 'увеличили')
    answer = answer.replace('WORd', 'уменьшили' if perc[1] < 0 else 'увеличили')
    answer = answer.replace('PROCENT', str(abs(perc[0])))
    answer = answer.replace('PROCENt', str(abs(perc[1])))
    answer = answer.replace('RESULT', ('уменьшилось на ' if dif < 0 else 'увеличилось на ') + str(abs(dif)))
    return [answer, answ]


inp = get_interface_input('numb(номеров в варианте, count, 14); numb(кол-во вариантов, variants, 2); chek(двусторонняя печать, doubleside); numb(максимальный ответ, maxansw, 1000); chek(нецелые числа, uglynumbs); chek(нецелый процент (малоэффективен), uglyperc); chek(прибавление и вычитание (не сочетается со след. пунктом), idmixer); chek(процент выше 100 (не сочетается с пред. пунктом), bigcent)',
                          description='Текстовые задачи на работу с процентами')

out = decode_output(inp) 

perpage = 9
dside = out['doubleside'] == '1'

answer = ''
answs = ''
for v in range(int(out['variants'])):
    for i in range(int(out['count'])):
        gen = generate(inp)
        answer += 'Задача ' + str(v + 1) + '.' + str(i + 1) + '\n' + gen[0] + '\n' * 2
        answs += str(v + 1) + '.' + str(i + 1) + ': ' + str(gen[1]) + '    '
        if answs.count(':') % 5 == 0:
            answs += '\n'
        if len(answs.split('\n')) % 43 == 0:
            answs += '\n{nextpage} '
        if (i + 1) % perpage == 0 and i != int(out['count']) - 1:
            answer += '{nextpage}'
    answer += '{nextpage}'
    if ceil(int(out['count']) / perpage) % 2 == 1 and dside:
        answer += '  {nextpage}'

answer += 'ОТВЕТЫ\n' + answs

#print(answer)
export_alternative(answer, font_size=15)
