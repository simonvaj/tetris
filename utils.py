
NUM_ROWS = 25
NUM_COLS = 12
BOX_WIDTH = 20
CANVAS_WIDTH = BOX_WIDTH * NUM_COLS
CANVAS_HEIGHT = BOX_WIDTH * NUM_ROWS
SCREEN_WIDTH = 2 * CANVAS_WIDTH
SCREEN_HEIGHT = CANVAS_HEIGHT + 22
DEFAULT_TIME_STEP = 300
TIME_STEP_REDUCE = 0.9995
MIN_TIME_STEP = 200
SAVED_STATE_NAME = 'save'

class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __getitem__(self, i):
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        assert False
    
    def __setitem__(self, i, value):
        if i == 0:
            self.x = value
        elif i == 1:
            self.y = value
        else:
            assert False
            
            
class Level(object):

    def __init__(self):
        self.theme = {}
        self.point_interval = []
        self.dt = 500
        
    def up(self):
        pass