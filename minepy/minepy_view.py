from tkinter import *
from tkinter import messagebox

from minepy.icon import Icon

''' Класс представления '''
class MinepyView():
    def __init__(self, game, minefield):
        self.game = game
        self.minefield = minefield
        self.game_name = "MinePy"   # название игры
        self.icon_size = 50         # размер иконки в пикселях

        self.initGUI()
        self.window.mainloop()

    # обновляет данные, полученные от модели
    def syncWithModel(self):
        for y in range(self.minefield.rows):
            for x in range(self.minefield.columns):
                label = Label(self.window,
                              image=self.minefield.getIconImage(x, y).icon,
                              borderwidth=0,
                              name=str(x) + " " + str(y))
                label.grid(column=x, row=y)

    # создает GUI
    def initGUI(self):
        self.window = Tk()
        self.window.title(self.game_name)
        self.window.iconbitmap("icons/minepy-icons.ico")
        self.window.resizable(False, False)
        self.setIcons()

        self.createMenuBar()

        self.syncWithModel()
        self.window.bind('<1>', self.pressLeftButton)
        self.window.bind('<3>', self.pressRightButton)

    # создает панель меню
    def createMenuBar(self):
        menu_bar = Menu(self.window)

        menu_game = Menu(menu_bar, tearoff=0)
        menu_game.add_command(label='Новая игра', command=self.newGame)

        settings = Menu(menu_bar, tearoff=0)
        settings.add_command(label="Простой 9х9", command=lambda: self.selectMode("easy"))
        settings.add_command(label="Средний 16х16", command=lambda: self.selectMode("middle"))
        settings.add_command(label="Эксперт 30х16", command=lambda: self.selectMode("expert"))

        menu_game.add_cascade(label='Уровень сложности', menu=settings)

        menu_game.add_separator()
        menu_game.add_command(label='Выход', command=self.window.quit)

        menu_bar.add_cascade(label='Игра', menu=menu_game)

        info_game = Menu(menu_bar, tearoff=0)
        info_game.add_command(label='Правила игры', command=lambda: self.createInfoDialog("rules"))
        info_game.add_command(label='Советы', command=lambda: self.createInfoDialog("advices"))

        menu_bar.add_cascade(label='Помощь', menu=info_game)
        self.window.config(menu=menu_bar)

    # обработка события проигрыша или победы
    def createDialog(self):
        messagebox.showinfo(self.game_name, self.minefield.getMessage())
        self.game.pressLeftButton(1, 1)
        self.syncWithModel()

    # обработка события выбора меню Правила игры / Советы
    def createInfoDialog(self, command):
        top = Toplevel(self.window)
        name = []
        top.grab_set()
        top.focus_set()
        top.resizable(False, False)

        txt = Text(top, wrap=WORD, font="Verdana 10", width=50, height=15)
        txt.insert(INSERT, self.game.readText(command, name))
        txt.configure(state='disabled')
        txt.pack(side=LEFT)

        top.title(name[0])

        scroll = Scrollbar(top, command=txt.yview)
        scroll.pack(side=LEFT, fill=Y)

        txt.config(yscrollcommand=scroll.set)

    # получение координат ЛКМ
    def pressLeftButton(self, event):
        x = self.window.winfo_pointerx()
        y = self.window.winfo_pointery()

        coordX = x - self.window.winfo_rootx()
        coordY = y - self.window.winfo_rooty()

        self.game.pressLeftButton(coordX // self.icon_size, coordY // self.icon_size)
        self.syncWithModel()

        if self.minefield.isGameOver():
            self.createDialog()

    # получение координат ПКМ
    def pressRightButton(self, event):

        x = self.window.winfo_pointerx()
        y = self.window.winfo_pointery()

        coordX = x - self.window.winfo_rootx()
        coordY = y - self.window.winfo_rooty()

        self.game.pressRightButton(coordX // self.icon_size, coordY // self.icon_size)
        self.syncWithModel()

    # устанавливает значение переменной icon для всех элементов перечисления
    def setIcons(self):
        for icon in list(Icon):
            icon.icon = self.getIcon(icon.name.lower())

    # возвращает изображение по пути
    def getIcon(self, iconName):
        file = "icons/" + iconName + ".png"
        image = PhotoImage(file=file)
        return image

    # запускает новую игру
    def newGame(self):
        self.destroyLabels()
        self.game.startNewGame()
        self.syncWithModel()

    # выбор сложности игры
    def selectMode(self, mode):
        self.destroyLabels()
        self.game.selectMode(mode)
        self.minefield = self.game.getMinefield()

        self.syncWithModel()

    # очищает игровое поле
    def destroyLabels(self):
        for y in range(self.minefield.rows):
            for x in range(self.minefield.columns):
                r = self.window.nametowidget(str(x) + " " + str(y))
                r.destroy()




