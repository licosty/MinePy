from minepy.minefield import Minefield

''' Класс контроллера '''
class MinepyGame():
    def __init__(self, minefield):
        self.minefield = minefield
        self.startNewGame()

    # инициализирует старт игры
    def startNewGame(self):
        self.minefield.startGame()

    # обработка события от нажатия ЛКМ
    def pressLeftButton(self, x, y):
        if self.minefield.isGameOver():
            self.startNewGame()
            return

        if self.minefield.isFirstStep():
            self.minefield.setFirstStep(x, y)

        self.minefield.setOpened(x, y)
        self.minefield.isWin()

    # обработка события от нажатия ПКМ
    def pressRightButton(self, x, y):
        self.minefield.toggleFlagged(x, y)

    # устанавливает значения игрового поля в зависимости от
    # выбранного уровня сложности
    def selectMode(self, mode):
        if mode == 'easy':
            self.minefield = Minefield()
            self.startNewGame()
        elif mode == 'middle':
            self.minefield = Minefield(16, 16, 40)
            self.startNewGame()
        elif mode == 'expert':
            self.minefield = Minefield(30, 16, 100)
            self.startNewGame()

    # читает текст из файла и возвращает его
    def readText(self, command, name):
        rules = ''
        filePath = ""

        if command == "rules":
            filePath = "text/rulesOfGame.txt"
            name.append("Правила игры")

        if command == "advices":
            filePath = "text/advices.txt"
            name.append("Советы")

        with open(filePath, encoding='utf-8') as rfile:
            for line in rfile:
                rules += line.strip() + '\n'
        return rules

    # возвращает объект игрового поля
    def getMinefield(self):
        return self.minefield