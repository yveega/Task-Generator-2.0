import pygame
from pygame.locals import *
import pygame_gui
import time
import os

# consts
HEIGHT = 600
WIDTH = 991

pygame.init()
pygame.font.init()


def my_index(arr, elem):
    for i in range(len(arr)):
        if arr[i][0] == elem:
            return i
    return -1


def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    if x < 0:
        return -1


def imload(name, pos=(0, 0)):
    img = pygame.image.load('Resource/Images/' + name)
    img.set_colorkey(img.get_at(pos))
    return img


def border(string):
    return string[string.find('(') + 1: string.rfind(')')]


"""
Извлекает значение внутри скобок в строке
string - исходная строка (обязана содержать хотя бы одну открывающую и закрывающую скобку в нужном порядке)
"""


def string_to_number(string):
    if len(string) == 0:
        return '0'
    answ = ''
    if string[0] == '-':
        answ = '-'
        string = string[1:]
    was_dot = False
    for i in range(0, len(string)):
        if string[i] in '.,' and i != 0 and not was_dot:
            was_dot = True
            answ = answ + '.'
        if string[i] in '1234567890':
            answ = answ + string[i]
    if len(answ) == 0:
        return '0'
    while answ[0] == 0:
        answ = answ[1:]
    if answ[0] == '.':
        while answ[1] == 0:
            answ = '-' + answ[2:]
    if answ[0] == '-':
        while answ[1] == 0:
            answ = '-' + answ[2:]
        if answ[1] == '.':
            while answ[1] == 0:
                answ = '-' + answ[2:]
    return answ


class UIElement:
    typ = 'None'
    name = ''
    ID = ''
    default = ''
    options = []

    def __init__(self, typ, name, manager, options=[], default='', ID=''):
        self.typ = typ
        self.name = name
        self.default = default
        self.options = options.copy()
        self.ID = ID
        self.manager = manager
        self.description = None

    def get_gui(self, rect):  # Возвращает объект GUI
        shift = 2
        if self.typ == 'chek':
            self.description = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((rect[0], rect[1] + 2), (rect[2] - rect[3] - 10, rect[3] - 2 * shift)),
                text=self.name,
                manager=self.manager,
                visible=True)
        else:
            self.description = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((rect[0], rect[1] + 2), (rect[2] // 2 - 30, rect[3] - 2 * shift)),
                text=self.name,
                manager=self.manager,
                visible=True)
        if self.typ == 'text':
            answ = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
                relative_rect=pygame.Rect((rect[0] + rect[2] // 2 - 20, rect[1]), (rect[2] // 2 + 20, rect[3])),
                manager=self.manager)
            answ.set_text(self.default)
            return answ, self.description
        if self.typ == 'numb':
            answ = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
                relative_rect=pygame.Rect((rect[0] + rect[2] // 2 - 20, rect[1]), (rect[2] // 2 + 20, rect[3])),
                manager=self.manager)
            answ.set_text(self.default)
            return answ, self.description
        if self.typ == 'list':
            return pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=self.options.copy(),
                                                                        starting_option=self.default,
                                                                        relative_rect=pygame.Rect(
                                                                            (rect[0] + rect[2] // 2 - 20, rect[1]),
                                                                            (rect[2] // 2 + 20, rect[3])),
                                                                        manager=self.manager), self.description
        if self.typ == 'radi':
            return pygame_gui.elements.UISelectionList(
                relative_rect=pygame.Rect((rect[0] + rect[2] // 2 - 20, rect[1]), (rect[2] // 2 + 20, rect[3])),
                item_list=self.options.copy(),
                manager=self.manager,
                allow_double_clicks=False,
                allow_multi_select=False), self.description
        if self.typ == 'chek':  # Да, я знаю, что здесь ошибка и правильно с точки зрения грамматики писать "check", но я специально сократил слово до 4 букв
            return pygame_gui.elements.UISelectionList(
                relative_rect=pygame.Rect((rect[0] + rect[2] - rect[3], rect[1]), (rect[3], rect[3])),
                item_list=[' '],
                manager=self.manager,
                allow_double_clicks=False,
                allow_multi_select=True), self.description


"""
Класс для временного хранения результатов расшифровки входной строки программы.
"""


def decode_uis(string, manager):
    answ = []
    arr = string.split(';')
    for com in arr:
        s = border(com).split(',')
        for i in range(len(s)):
            if s[i][0] == ' ':
                s[i] = s[i][1:]
        if com.replace(' ', '')[:4] == 'text':
            answ.append(UIElement('text', name=s[0], default=s[2], ID=s[1], manager=manager))
        if com.replace(' ', '')[:4] == 'numb':
            answ.append(UIElement('numb', name=s[0], default=s[2], ID=s[1], manager=manager))
        if com.replace(' ', '')[:4] == 'list':
            answ.append(UIElement('list', name=s[0], default=s[2], ID=s[1], options=s[3:], manager=manager))
        if com.replace(' ', '')[:4] == 'radi':
            answ.append(UIElement('radi', name=s[0], ID=s[1], options=s[2:], manager=manager))
        if com.replace(' ', '')[:4] == 'chek':
            answ.append(UIElement('chek', name=s[0], ID=s[1], manager=manager))
    return answ


"""
Функция для расшифровки входной строки (ввода) программы
"""


# TODO: приближение --- желательно
# TODO: количество задач и вариантов --- до следующего раза
# TODO: выбор генератора --- потом
# TODO: результат словарь


class Drawer:
    def __init__(self, params='', description='Нет описания генератора :('):
        self.description = description.replace('\n', '<br>')
        # self.UIs = decode_uis(params, s)
        self.scr = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('GRIT-Z')  # Generator of Randomized Instances of Tasks - Zero edition
        self.reset(params)
        self.tm = time.monotonic()
        self.bg = pygame.image.load('Resource/Images/ground.jpg')
        self.flag = imload('flag.bmp')
        self.cross = imload('cross.bmp')
        self.no_pages_label = pygame.font.SysFont('Calibri', 18)
        self.no_pages_label = self.no_pages_label.render('Нет страниц для предпросмотра', True, (0, 0, 0))
        self.current_page = 0
        self.total_pages = 0
        self.scrolls = 0
        self.page_scale = 1
        self.page_topleft = (0, 0)
        self.backward_button = pygame_gui.elements.ui_button.UIButton(
            manager=self.manager, relative_rect=pygame.Rect((650, 567), (25, 25)), text='<', visible=0)
        self.pages_num_input = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect((750, 565), (50, 25)), manager=self.manager, visible=0)
        self.forward_button = pygame_gui.elements.ui_button.UIButton(
            manager=self.manager, relative_rect=pygame.Rect((886, 567), (25, 25)), text='>', visible=0)
        self.pages_num_input.set_text('1')
        self.gen_tab = pygame_gui.elements.ui_button.UIButton(manager=self.manager,
                                                              relative_rect=pygame.Rect((20, 550), (100, 30)),
                                                              text='генераторы')
        self.params_tab = pygame_gui.elements.ui_button.UIButton(manager=self.manager,
                                                                 relative_rect=pygame.Rect((118, 550), (100, 30)),
                                                                 text='параметры')
        self.params_tab.disable()

    def pages_input_upd(self, page):
        try:
            page = int(page)
        except ValueError:
            return
        if page < 1 or page > self.total_pages:
            return
        self.current_page = page - 1
        self.pages_num_input.set_text(str(page))

    def pages_upd(self):
        if 'pages.txt' in os.listdir(os.getcwd()):
            f = open('pages.txt', 'r')
            pages_images = [pygame.image.load(i.strip()) for i in f]
            f.close()
            self.total_pages = len(pages_images)
            page_scaled = pygame.transform.smoothscale(pages_images[self.current_page],
                                                       (int(self.page_scale * 540 / 2 ** 0.5),
                                                        int(self.page_scale * 540)))
            self.scr.blit(page_scaled, (590, 20), (*self.page_topleft, int(540 / 2 ** 0.5), 540))
            self.pages_num_input.visible = 1
            self.forward_button.visible = 1
            self.backward_button.visible = 1
            self.total_pages_label = pygame.font.SysFont('Calibri', 18)
            self.total_pages_label = self.total_pages_label.render(f' / {len(pages_images)}', True, (0, 0, 0))
            self.scr.blit(self.total_pages_label, (800, 570))
        else:
            self.pages_num_input.visible = 0
            self.forward_button.visible = 0
            self.backward_button.visible = 0
            self.scr.blit(self.no_pages_label, (670, 300))

    def page_topleft_upd(self, rel):
        self.page_topleft = (self.page_topleft[0] - rel[0], self.page_topleft[1] - rel[1])
        self.page_topleft = (int(max(0, min((self.page_scale - 1) * 540 / 2 ** 0.5 + 1, self.page_topleft[0]))),
                             int(max(0, min((self.page_scale - 1) * 540 + 1, self.page_topleft[1]))))

    def page_scale_upd(self, val):
        self.page_scale = max(1, min(8, self.page_scale + val))

    def reset(self, params):  # Пересоздаёт меню с другими настройками (ввод)
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'Resource/Styles/theme.json')
        self.desc_textbox = pygame_gui.elements.ui_text_box.UITextBox(relative_rect=pygame.Rect((20, 20), (550, 200)),
                                                                      html_text=self.description, manager=self.manager)
        self.uis = decode_uis(params, self.manager)
        self.guis = []
        curent_position = 240
        self.rects = []
        for i, ui in enumerate(self.uis):
            if ui.typ == 'radi':
                height = 22 * (len(ui.options))
            else:
                height = 26
            self.guis.append(ui.get_gui([20, curent_position, 250 + 300, height]))
            self.rects.append([20, curent_position, 250 + 300, height])
            curent_position += height + 3

        self.generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, curent_position + 37), (550, 50)),
            text='Generate!',
            manager=self.manager)
        self.versions = UIElement('numb', 'количество вариантов:', self.manager, default='1',
                                  ID='кол-во вариантов:')
        self.versions = self.versions.get_gui([20, 320, 550, 25])
        self.versions[0].disable()
        self.versions[0].visible = 0
        self.versions[1].disable()
        self.versions[1].visible = 0
        self.tasks = UIElement('numb', 'количество задач:', self.manager, default='1',
                               ID='кол-во вариантов:')
        self.tasks = self.tasks.get_gui([20, 348, 550, 25])
        self.tasks[0].disable()
        self.tasks[0].visible = 0
        self.tasks[1].disable()
        self.tasks[1].visible = 0

    def get_values(self):  # Возвращает массив значений элементов интерфейса
        answ = []
        ids = [x.ID for x in self.uis]
        for ui in self.guis:
            try:
                answ.append(ui[0].selected_option)
            except:
                try:
                    answ.append(ui[0].get_text())
                except:
                    try:
                        answ.append(str(ui[0].get_single_selection()))
                    except:
                        answ.append(str(len(ui[0].get_multi_selection())))
        use_brackets = False
        if use_brackets:
            return '{' + ', '.join(
                ['\'' + str(ids[i]) + '\' : \'' + str(answ[i]) + '\'' for i in range(len(ids))]) + '}'
        params = ', '.join([str(ids[i]) + ' : ' + str(answ[i]) for i in range(len(ids))])
        try:
            versions = int(self.versions[0].get_text())
        except ValueError:
            versions = 1
        try:
            tasks = int(self.tasks[0].get_text())
        except ValueError:
            tasks = 1
        return {'params': params, 'versions': versions, 'tasks': tasks}  # version - вариант

    def operate_events(self):  # Обрабатывает события пользователя.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'stop'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pages_input_upd(self.current_page + 1 - 1)
                if event.key == pygame.K_RIGHT:
                    self.pages_input_upd(self.current_page + 1 + 1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                ctrl = pygame.key.get_mods() & pygame.KMOD_CTRL
                if ctrl:
                    scale = self.page_scale
                    if event.button == 4:
                        self.page_scale_upd(0.5)
                    if event.button == 5:
                        self.page_scale_upd(-0.5)
                    x, y = self.page_topleft[0] + event.pos[0] - 590, self.page_topleft[1] + event.pos[1] - 20
                    self.page_topleft_upd(
                        (x - x / scale * self.page_scale, y - y / scale * self.page_scale))
                else:
                    if event.button == 4:
                        self.scrolls -= 1
                    if event.button == 5:
                        self.scrolls += 1
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0] == 1:
                    if pygame.Rect((590, 20), (int(540 / 2 ** 0.5), 540)).collidepoint(event.pos):
                        self.page_topleft_upd(event.rel)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.generate_button:
                        self.pages_num_input.set_text('1')
                        self.current_page = 0
                        self.scrolls = 0
                        try:
                            os.remove(os.getcwd() + '/pages.txt')
                        except FileNotFoundError:
                            pass
                        return self.get_values()
                    if event.ui_element == self.backward_button:
                        self.pages_input_upd(self.current_page + 1 - 1)
                    if event.ui_element == self.forward_button:
                        self.pages_input_upd(self.current_page + 1 + 1)
                    if event.ui_element == self.gen_tab:
                        self.generate_button.disable()
                        self.generate_button.visible = 0
                        self.desc_textbox.disable()
                        self.desc_textbox.visible = 0
                        for i in self.guis:
                            i[0].disable()
                            i[0].visible = 0
                            i[1].disable()
                            i[1].visible = 0
                        self.versions[0].enable()
                        self.versions[0].visible = 1
                        self.versions[1].enable()
                        self.versions[1].visible = 1
                        self.tasks[0].enable()
                        self.tasks[0].visible = 1
                        self.tasks[1].enable()
                        self.tasks[1].visible = 1
                        self.gen_tab.disable()
                        self.params_tab.enable()
                    if event.ui_element == self.params_tab:
                        self.generate_button.enable()
                        self.generate_button.visible = 1
                        self.desc_textbox.enable()
                        self.desc_textbox.visible = 1
                        for i in self.guis:
                            i[0].enable()
                            i[0].visible = 1
                            i[1].enable()
                            i[1].visible = 1
                        self.versions[0].disable()
                        self.versions[0].visible = 0
                        self.versions[1].disable()
                        self.versions[1].visible = 0
                        self.tasks[0].disable()
                        self.tasks[0].visible = 0
                        self.tasks[1].disable()
                        self.tasks[1].visible = 0
                        self.params_tab.disable()
                        self.gen_tab.enable()
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.pages_num_input:
                        self.pages_input_upd(self.pages_num_input.get_text())
                        continue
                    else:
                        i = my_index(self.guis, event.ui_element)
                        if self.uis[i].typ == 'numb':
                            self.guis[i][0].set_text(string_to_number(self.guis[i][0].get_text()))
            self.manager.process_events(event)

    def tick(self):  # Функция для обновления. Должна вызываться каждый проход основного цикла программы.
        TM = time.monotonic()
        delta = TM - self.tm
        self.tm = TM
        res = self.operate_events()
        if abs(self.scrolls) >= 2:
            self.pages_input_upd(self.current_page + 1 + sign(self.scrolls))
            self.scrolls = 0
        self.manager.update(delta)
        self.scr.blit(self.bg, (0, 0))
        self.manager.draw_ui(self.scr)
        for i in range(len(self.uis)):
            if self.uis[i].typ == 'chek':
                img = self.cross
                if len(self.guis[i][0].get_multi_selection()):
                    img = self.flag
                rect = self.rects[i]
                shift = 3
                pos_x = rect[0] + rect[2] - rect[3] + shift
                pos_y = rect[1] + shift
                self.scr.blit(pygame.transform.scale(img, [rect[3] - 2 * shift] * 2), [pos_x, pos_y])
        self.pages_upd()
        pygame.display.update()
        return res


"""
Основной класс программы
"""


def get_interface_input(params='', description='Нет описания генератора :('):
    log = open('Logs/Interface_log.txt', 'w')
    print('params -', params, '\ndescription -', description, '\n', file=log)
    log.close()
    drw = Drawer(params, description=description)
    kg = True  # Условие основного цикла программы
    while kg:  # ОЦП (Основной Цикл Программы)
        res = drw.tick()  # Обновление интерфейса и приём команд пользователя. Для пересоздания интерфейса используется функция reset("новый_ввод")
        # Обработка вывода интерфейса
        if res == 'stop':
            kg = False
            pygame.quit()
            log = open('Logs/Interface_log.txt', 'r')
            text = log.read()
            log.close()
            log = open('Logs/Interface_log.txt', 'w')
            print(text, file=log)
            print('Program closed by user. None returned.', file=log)
            log.close()
            return None
        elif res is not None:
            pygame.quit()
            log = open('Logs/Interface_log.txt', 'r')
            text = log.read()
            log.close()
            log = open('Logs/Interface_log.txt', 'w')
            print(text, file=log)
            print('Generate event got. Params -', res, file=log)
            log.close()
            return res