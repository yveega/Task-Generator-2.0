

def reformat(tasks, answers, **kwargs):
    # font_size = 20
    # ans_after_each = False
    # ans_end = True
    # k_versions = 1
    # flip_answers = True
    # blank_pages = False
    # k_vars_on_page = 1
    res = "{font_size = " + str(kwargs.get("font_size", 20)) + "}\n"
    k_in_ver = len(tasks) // kwargs.get("k_versions", 1)
    num_task = 1
    for i, task in enumerate(tasks):
        if i % k_in_ver == 0:
            res += "{binding='center'} Вариант " + str(i // k_in_ver + 1) + "\n"
        res += "{italic=True}Задание №" + str(i % k_in_ver + 1) + '.{italic=False}\n'
        res += "{math}" + task + "{math}\n"
        if kwargs.get("ans_after_each", False):
            if kwargs.get("flip_answers", True):
                res += "{flipped=True}{math}c(t(Ответ: ))(" + answers[i] + "){math}\n{flipped=False}"
            else:
                res += "{math}c(t(Ответ: ))(" + answers[i] + "){math}\n"
        if (i + 1) % k_in_ver == 0:
            res += "{nextpage}"
    if kwargs.get("ans_end", True):
        res += "ОТВЕТЫ\n"
        for i, ans in enumerate(answers):
            if i % k_in_ver == 0:
                res += "Вариант " + str(i // k_in_ver + 1) + "\n"
            res += "{math}c(t(№" + str(i % k_in_ver + 1) + ": ))(" + ans + "){math}\n"
    return res

# t1 = ['c(c(c(t(x))(i()(2)))(t(- 32 x )))(t(+ 256 = 0))', 'c(c(c(t(4 x))(i()(2)))(t(+ 12 x )))(t(+ 9 = 0))', 'c(c(c(t(x))(i()(2)))(t(- 34 x )))(t(+ 289 = 0))', 'c(c(c(t(4 x))(i()(2)))(t(- 68 x )))(t(+ 289 = 0))', 'c(c(c(t(x))(i()(2)))(t(- 34 x )))(t(+ 289 = 0))', 'c(c(c(t(9 x))(i()(2)))(t(- 48 x )))(t(+ 64 = 0))']
# a1 = ['c(t(x = ))(t(16))', 'c(t(x = ))(- (-3 / 2))', 'c(t(x = ))(t(17))', 'c(t(x = ))(t(17 / 2))', 'c(t(x = ))(t(17))', 'c(t(x = ))(t(8 / 3))']
# print(reformat(t1, a1))
