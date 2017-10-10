"""Definitions of tetromino objects, the small pieces that are falling down!"""
from utils import NUM_COLS

TETRO_COLORMAP = [str('#%02x%02x%02x' % (70, 70, 70)),
                  str('#%02x%02x%02x' % (100, 100, 100)),
                  str('#%02x%02x%02x' % (200, 200, 200)),
                  str('#%02x%02x%02x' % (240, 240, 240)),
                  str('#%02x%02x%02x' % (125, 125, 125)),
                  str('#%02x%02x%02x' % (175, 175, 175)),
                  str('#%02x%02x%02x' % (220, 220, 220))]

class Position(object):
    """Simple 2-component position class."""

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

class Tetromino(object):
    """A tetromino describes falling piece in tetris!"""

    tetro_id = 0

    def __init__(self, x=NUM_COLS/2, y=-1):
        self.blocks = [None] * 4
        self.pos = Position(x, y)
        self.rotation = 0
        self.tetro_id = Tetromino.tetro_id
        Tetromino.tetro_id += 1

    def rotate(self):
        """Rotation: switch between 2 or more tetromino states."""
        self.rotation += 1
        self.rotation %= 4

    def update(self):
        """Update the tetromino: it is always falling down!"""
        self.pos.y += 1

    def __eq__(self, rhs):
        return self.tetro_id == rhs.tetro_id

class SquareTetromino(Tetromino):
    """Square 2x2 tetromino."""
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = TETRO_COLORMAP[0]
        self.blocks[0] = 0, 0
        self.blocks[1] = 1, 0
        self.blocks[2] = 0, 1
        self.blocks[3] = 1, 1

class StraightTetromino(Tetromino):
    """Straight tetromino has 4 blocks in a row."""

    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = TETRO_COLORMAP[1]
        self.rotate()

    def rotate(self):
        """Switch between "vertical" and "horizontal" state."""
        if self.rotation % 2 == 0:
            # Vertical state
            self.blocks[0] = 0, -2
            self.blocks[1] = 0, -1
            self.blocks[2] = 0, 0
            self.blocks[3] = 0, 1
        else:
            # Horizontal state
            self.blocks[0] = -1, 0
            self.blocks[1] = 0, 0
            self.blocks[2] = 1, 0
            self.blocks[3] = 2, 0
        super(StraightTetromino, self).rotate()

class TTetromino(Tetromino):
    """Tetromino with 4 blocks, looking like a T.
    This tetromino has 4 different states."""

    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = TETRO_COLORMAP[2]
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
    """A mirrored L tetromino with 2 different states."""

    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = TETRO_COLORMAP[3]
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
    """An L-shaped tetromino with 2 different states."""
    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = TETRO_COLORMAP[4]
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

class ZTetromino(Tetromino):
    """An Z-shaped tetromino."""

    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = TETRO_COLORMAP[5]
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
        super(ZTetromino, self).rotate()

class STetromino(Tetromino):
    """An S-shaped tetromino."""

    def __init__(self, x=NUM_COLS/2-1, y=-1):
        Tetromino.__init__(self, x, y)
        self.color = TETRO_COLORMAP[6]
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
        super(STetromino, self).rotate()
