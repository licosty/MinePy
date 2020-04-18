from enum import Enum

''' Перечисление возможных элементов поля '''
class Icon(Enum):
    ZERO = 0
    NUM1 = 1
    NUM2 = 2
    NUM3 = 3
    NUM4 = 4
    NUM5 = 5
    NUM6 = 6
    NUM7 = 7
    NUM8 = 8
    TAIL = 9
    OPENED = 10
    CLOSED = 11
    FLAGGED = 12
    INFORM = 13
    STEPPED = 14
    NOTAIL = 15

    def __init__(self, icon=""):
        # хранит изображение
        self.icon = icon

    # возвращает следующую в перечислении иконку
    def getNextIcon(self):
        return list(Icon)[self.value+1]
