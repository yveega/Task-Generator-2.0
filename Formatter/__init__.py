

def reformat(tasks, answers, ans_after_each=False, ans_end=True, font_size=20):
    res = "{font_size = " + str(font_size) + "}"
    for i, task in enumerate(tasks):
        res += "Задание №" + str(i + 1) + '.\n'
        res += "{math}" + task + "{math}\n"
        if ans_after_each:
            res += "Ответ: {math}" + answers[i] + "{math}\n"
        res += "{nextpage}"
    if ans_end:
        res += "ОТВЕТЫ\n"
        for i, ans in enumerate(answers):
            res += "№" + str(i + 1) + ": {math}" + ans + "{math}\n"
    return res

# t1 = ['c(c(c(t(x))(i()(2)))(t(- 32 x )))(t(+ 256 = 0))', 'c(c(c(t(4 x))(i()(2)))(t(+ 12 x )))(t(+ 9 = 0))', 'c(c(c(t(x))(i()(2)))(t(- 34 x )))(t(+ 289 = 0))', 'c(c(c(t(4 x))(i()(2)))(t(- 68 x )))(t(+ 289 = 0))', 'c(c(c(t(x))(i()(2)))(t(- 34 x )))(t(+ 289 = 0))', 'c(c(c(t(9 x))(i()(2)))(t(- 48 x )))(t(+ 64 = 0))']
# a1 = ['c(t(x = ))(t(16))', 'c(t(x = ))(- (-3 / 2))', 'c(t(x = ))(t(17))', 'c(t(x = ))(t(17 / 2))', 'c(t(x = ))(t(17))', 'c(t(x = ))(t(8 / 3))']
# print(reformat(t1, a1))
