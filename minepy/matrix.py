''' Вспомогательный класс матрицы поля'''
class Matrix():
    def __init__(self, defaultIcon, columns, rows):
        # заполнение матрицы иконкой по умолчанию при старте новой игры
        self.matrix = [[defaultIcon for _ in range(rows)] for _ in range(columns)]
        self.columns = columns
        self.rows = rows

    # возвращает иконку по координатам
    def getIconByCoords(self, x, y):
        if self.isNotBound(x, y):
            return self.matrix[x][y]
        return None

    # устанавливает иконку по координатам
    def setIconByCoords(self, x, y, icon):
        if self.isNotBound(x, y):
            self.matrix[x][y] = icon

    # проверяет выходит ли координата за пределы поля
    def isNotBound(self, x, y):
        return (0 <= x < self.columns) & (0 <= y < self.rows)

