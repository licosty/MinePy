from random import randint

from minepy.icon import Icon
from minepy.matrix import Matrix

''' Класс модели '''
class Minefield():
    def __init__(self, columns=9, rows=9, tails=10):
        self.columns = columns      # количество столбцов
        self.rows = rows            # количество строк
        self.tails = tails          # количество бомб
        self.firstStep = [-1, -1]   # координаты первого шага

    # инициализирует игровое поле
    def startGame(self):
        self.placeTails()
        self.placeUpperLayer()
        self.count_cells = self.columns * self.rows
        self.game_over = False
        self.setFirstStep(-1, -1)

    # размещает бомбы на поле
    def placeTails(self):
        self.tail_layer = Matrix(Icon.ZERO, self.columns, self.rows)
        for _ in range(self.tails):
            self.placeTail()

    # размещает одну бомбу в случайном месте
    def placeTail(self):
        while (True):
            coord = self.getRandomCoord()
            if (coord[0] == self.firstStep[0]) & (coord[1] == self.firstStep[1]):
                continue
            if Icon.TAIL == self.tail_layer.getIconByCoords(coord[0], coord[1]):
                continue

            self.tail_layer.setIconByCoords(coord[0], coord[1], Icon.TAIL)

            for array in self.getCoordsAround(coord[0], coord[1]):
                if Icon.TAIL != self.tail_layer.getIconByCoords(array[0], array[1]):
                    self.tail_layer.setIconByCoords(array[0], array[1],
                                                    self.tail_layer.getIconByCoords(array[0], array[1]).getNextIcon())

            break

    # получить случайную координату
    def getRandomCoord(self):
        coord = []
        coord.append(randint(0, self.columns-1))
        coord.append(randint(0, self.rows-1))
        return coord

    # инициализирует верхний уровень игрового поля
    def placeUpperLayer(self):
        self.upper_layer = Matrix(Icon.CLOSED, self.columns, self.rows)

    # возвращает массив координат вокруг ячейки
    def getCoordsAround(self, coordX, coordY):
        listCoords = []
        for x in range(coordX - 1, coordX + 2):
            for y in range(coordY - 1, coordY + 2):
                if self.tail_layer.isNotBound(x, y):
                    if (x != coordX) | (y != coordY):
                        listCoords.append([x, y])
        return listCoords

    # переключает иконки при клике на ПКМ
    def toggleFlagged(self, x, y):
        if self.upper_layer.getIconByCoords(x, y) == Icon.FLAGGED:
            self.upper_layer.setIconByCoords(x, y, Icon.INFORM)
        elif self.upper_layer.getIconByCoords(x, y) == Icon.INFORM:
            self.upper_layer.setIconByCoords(x, y, Icon.CLOSED)
        elif self.upper_layer.getIconByCoords(x, y) == Icon.CLOSED:
            self.upper_layer.setIconByCoords(x, y, Icon.FLAGGED)

    # открывает ячейку
    def setOpened(self, x, y):
        icon_upper = self.upper_layer.getIconByCoords(x, y)

        if (icon_upper == Icon.FLAGGED) | (icon_upper == Icon.INFORM):
            return
        elif icon_upper == Icon.OPENED:
            self.openAroundNumber(x, y)
        elif icon_upper == Icon.CLOSED:
            icon_tail = self.tail_layer.getIconByCoords(x, y)

            if icon_tail == Icon.ZERO:
                self.openCellsAround(x, y)
            elif icon_tail == Icon.TAIL:
                self.openAllBombs(x, y)
            else:
                self.upper_layer.setIconByCoords(x, y, Icon.OPENED)
                self.countCellsDecrement()

    # открывает ячейки вокруг цифры, если рядом установлен флаг
    def openAroundNumber(self, x, y):
        if self.getCountFlagsAround(x, y) == self.tail_layer.getIconByCoords(x, y).value:
            for around in self.getCoordsAround(x, y):
                if self.upper_layer.getIconByCoords(around[0], around[1]) == Icon.CLOSED:
                    self.setOpened(around[0], around[1])

    # возвращает количество флагов вокруг цифры
    def getCountFlagsAround(self, x, y):
        count = 0
        for around in self.getCoordsAround(x, y):
            if self.upper_layer.getIconByCoords(around[0], around[1]) == Icon.FLAGGED:
                count += 1

        return count

    # открывает вокруг пустой ячейки все другие пустые ячейки, если таковые есть,
    # до первых встреченных цифр
    def openCellsAround(self, x, y):
        self.upper_layer.setIconByCoords(x, y, Icon.OPENED)
        self.countCellsDecrement()
        for around in self.getCoordsAround(x, y):
            self.setOpened(around[0], around[1])

    # показывает все неотмеченные флагом бомбы в случае проигрыша
    def openAllBombs(self, bombX, bombY):
        self.game_over = True
        self.message = "Шшш! Одна змея сегодня зла"
        self.upper_layer.setIconByCoords(bombX, bombY, Icon.STEPPED)

        for x in range(self.columns):
            for y in range(self.rows):
                if self.tail_layer.getIconByCoords(x, y) == Icon.TAIL:
                    if self.upper_layer.getIconByCoords(x, y) == Icon.CLOSED:
                        self.upper_layer.setIconByCoords(x, y, Icon.OPENED)

                else:
                    if self.upper_layer.getIconByCoords(x, y) == Icon.FLAGGED:
                        self.upper_layer.setIconByCoords(x, y, Icon.NOTAIL)

    # проверяет является ли шелчок первым игровым ходом
    def isFirstStep(self):
        return self.firstStep[0] == -1 & self.firstStep[1] == -1

    # устанавливает координаты первого шага и,
    # если там бомба, перерасполагает их бомбы
    def setFirstStep(self, x, y):
        self.firstStep[0] = x
        self.firstStep[1] = y

        if self.tail_layer.getIconByCoords(x, y) == Icon.TAIL:
            self.placeTails()

    # возвращает статус игры
    def isGameOver(self):
        return self.game_over

    # устанавливает окончание игры в случае победы
    def isWin(self):
        if self.count_cells == self.tails:
            self.game_over = True
            self.message = "Поздравляю! Никого не покусали!"

    # уменьшает количество закрытых ячеек на 1
    def countCellsDecrement(self):
        self.count_cells -= 1

    # возвращает иконку c верхнего или нижнего уровня по координатам
    def getIconImage(self, x, y):
        if self.upper_layer.getIconByCoords(x, y) == Icon.OPENED:
            return self.tail_layer.getIconByCoords(x, y)
        return self.upper_layer.getIconByCoords(x, y)

    # возвращает сообщение для диалогового окна
    def getMessage(self):
        return self.message
