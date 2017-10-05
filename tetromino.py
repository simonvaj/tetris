from utils import *


themes = []
#themes.append()

g_cmap = [str('#%02x%02x%02x' % (70,70,70)),
          str('#%02x%02x%02x' % (100,100,100)),
          str('#%02x%02x%02x' % (200,200,200)),
          str('#%02x%02x%02x' % (240,240,240)),
          str('#%02x%02x%02x' % (125,125,125)),
          str('#%02x%02x%02x' % (175,175,175)),
          str('#%02x%02x%02x' % (220,220,220))]

class Tetromino(object):
    _id = 0

    def __init__(self, x=NUM_COLS/2, y=-1):
    
        self.blocks = [None] * 4
        self.pos = Position(x, y)
        self.rotation = 0
        self.id = Tetromino._id
        Tetromino._id += 1

    def rotate(self):
        self.rotation += 1
        self.rotation %= 4
        
    def update(self):
        self.pos.y += 1
        
    def __eq__(self, rhs):
        return self.id == rhs.id
        
class SquareTetromino(Tetromino):
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = g_cmap[0]
        self.blocks[0] = 0, 0
        self.blocks[1] = 1, 0
        self.blocks[2] = 0, 1
        self.blocks[3] = 1, 1
        
class StraightTetromino(Tetromino):
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = g_cmap[1]
        self.rotate()

    def rotate(self):
        if self.rotation % 2 == 0:
            """ Vertical state """
            self.blocks[0] = 0, -2
            self.blocks[1] = 0, -1
            self.blocks[2] = 0, 0
            self.blocks[3] = 0, 1
        else:
            """ Horizontal state """
            self.blocks[0] = -1, 0
            self.blocks[1] = 0, 0
            self.blocks[2] = 1, 0
            self.blocks[3] = 2, 0
        super(StraightTetromino, self).rotate()
        
class TTetromino(Tetromino):
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = g_cmap[2]
        self.rotate()

    def rotate(self):
        if self.rotation == 0:
            self.blocks[0] = 0, 0
            self.blocks[1] = -1, 0
            self.blocks[2] = 1, 0
            self.blocks[3] = 0, 1
        elif self.rotation == 1:
            self.blocks[0] = 0, 0
            self.blocks[1] = 0, 1
            self.blocks[2] = 0, -1
            self.blocks[3] = 1, 0
        elif self.rotation == 2:
            self.blocks[0] = 0, -1
            self.blocks[1] = 0, 0
            self.blocks[2] = -1, 0
            self.blocks[3] = 1, 0
        elif self.rotation == 3:
            self.blocks[0] = -1, 0
            self.blocks[1] = 0, 0
            self.blocks[2] = 0, -1
            self.blocks[3] = 0, 1
        super(TTetromino, self).rotate()
        
class JTetromino(Tetromino):
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = g_cmap[3]
        self.rotate()

    def rotate(self):
        if self.rotation == 0:
            self.blocks[0] = 0, -1
            self.blocks[1] = 0, 0
            self.blocks[2] = 0, 1
            self.blocks[3] = -1, 1
        elif self.rotation == 1:
            self.blocks[0] = -1, 0
            self.blocks[1] = 0, 0
            self.blocks[2] = 1, 0
            self.blocks[3] = 1, 1
        elif self.rotation == 2:
            self.blocks[0] = 0, -1
            self.blocks[1] = 0, 0
            self.blocks[2] = 0, 1
            self.blocks[3] = 1, -1
        elif self.rotation == 3:
            self.blocks[0] = -1, -1
            self.blocks[1] = -1, 0
            self.blocks[2] = 0, 0
            self.blocks[3] = 1, 0
        super(JTetromino, self).rotate()
        
class LTetromino(Tetromino):
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = g_cmap[4]
        self.rotate()

    def rotate(self):
        if self.rotation == 0:
            self.blocks[0] = 0, -1
            self.blocks[1] = 0, 0
            self.blocks[2] = 0, 1
            self.blocks[3] = 1, 1
        elif self.rotation == 1:
            self.blocks[0] = -1, 0
            self.blocks[1] = 0, 0
            self.blocks[2] = 1, 0
            self.blocks[3] = 1, -1
        elif self.rotation == 2:
            self.blocks[0] = -1, -1
            self.blocks[1] = 0, -1
            self.blocks[2] = 0, 0
            self.blocks[3] = 0, 1
        elif self.rotation == 3:
            self.blocks[0] = -1, 1
            self.blocks[1] = -1, 0
            self.blocks[2] = 0, 0
            self.blocks[3] = 1, 0
        super(LTetromino, self).rotate()
        
class STetromino(Tetromino):
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = g_cmap[5]
        self.rotate()

    def rotate(self):
        if self.rotation % 2 == 0:
            self.blocks[0] = 0, 0
            self.blocks[1] = 1, 0
            self.blocks[2] = 0, 1
            self.blocks[3] = -1, 1
        else:
            self.blocks[0] = 0, 0
            self.blocks[1] = 0, -1
            self.blocks[2] = 1, 0
            self.blocks[3] = 1, 1
        super(STetromino, self).rotate()
        
class ZTetromino(Tetromino):
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = g_cmap[6]
        self.rotate()

    def rotate(self):
        if self.rotation % 2 == 0:
            self.blocks[0] = 0, 0
            self.blocks[1] = -1, 0
            self.blocks[2] = 0, 1
            self.blocks[3] = 1, 1
        else:
            self.blocks[0] = 0, 0
            self.blocks[1] = 0, 1
            self.blocks[2] = 1, 0
            self.blocks[3] = 1, -1
        super(ZTetromino, self).rotate()