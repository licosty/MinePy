from minepy.minefield import Minefield
from minepy.minepy_game import MinepyGame
from minepy.minepy_view import MinepyView

''' Точка старта приложения '''
model = Minefield()
controller = MinepyGame(model)
view = MinepyView(controller, model)
