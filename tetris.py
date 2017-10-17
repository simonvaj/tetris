"""A fun and family-friendly tetris game!"""
import Tkinter as tk
import tkFont
import random
import time
import numpy as np
import tetromino

NUM_ROWS = 25
NUM_COLS = 12
BOX_WIDTH = 20
CANVAS_WIDTH = BOX_WIDTH * NUM_COLS
CANVAS_HEIGHT = BOX_WIDTH * NUM_ROWS
SCREEN_WIDTH = 2 * CANVAS_WIDTH
SCREEN_HEIGHT = CANVAS_HEIGHT + 22
TIME_STEP = 300
TIME_STEP_REDUCE = 0.9995
MIN_TIME_STEP = 200
SAVED_STATE_NAME = 'save'
KEYDOWN_WAIT_TIME = 0.5

def calculate_points(num_completed_rows):
    """Return appropriate no. of points given no- of completed
    rows."""
    if num_completed_rows < 1:
        return 0
    elif num_completed_rows == 1:
        return 200
    elif num_completed_rows == 2:
        return 500
    elif num_completed_rows == 3:
        return 1100
    return 2000

class Tetris(object):
    """The tetris game! Contains the game logic."""

    def __init__(self, nrows, ncols):
        self.nrows = nrows
        self.ncols = ncols
        self.points = 0

        # Dead blocks are blocks that don't move
        #pylint: disable=unused-variable
        self.dead_blocks = [[None for i in xrange(self.ncols)]
                                  for j in xrange(self.nrows)]
        self.curtetromino = None

    def reset(self):
        """Reset the game."""
        self.points = 0
        self.curtetromino = None
        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                self.dead_blocks[i][j] = None

    def spawn_tetromino(self):
        """Spawn a new, random tetromino."""
        #pylint: disable=invalid-name
        r = random.randint(0, 6)
        if r == 0:
            self.curtetromino = tetromino.SquareTetromino()
        elif r == 1:
            self.curtetromino = tetromino.StraightTetromino()
        elif r == 2:
            self.curtetromino = tetromino.TTetromino()
        elif r == 3:
            self.curtetromino = tetromino.JTetromino()
        elif r == 4:
            self.curtetromino = tetromino.LTetromino()
        elif r == 5:
            self.curtetromino = tetromino.STetromino()
        elif r == 6:
            self.curtetromino = tetromino.ZTetromino()
        self.curtetromino.pos = tetromino.Position(NUM_COLS/2, -1)

    def is_game_over(self):
        """Check if there are dead blocks at the ceiling."""
        for xpos in xrange(self.ncols):
            if self.dead_blocks[0][xpos] is not None:
                return True
        return False

    def move_left(self):
        """Move the current tetromino to the left."""
        can_move_left = True
        for block in self.curtetromino.blocks:
            xpos = self.curtetromino.pos[0] + block[0]
            ypos = self.curtetromino.pos[1] + block[1]
            if xpos <= 0:
                can_move_left = False
                break

            if self.dead_blocks[ypos][xpos - 1] is not None \
                    and xpos >= 1 and xpos < self.ncols \
                    and ypos >= 0 and ypos < self.nrows:
                can_move_left = False
                break

        if can_move_left:
            self.curtetromino.pos.x -= 1

    def move_right(self):
        """Move the current tetromino to the right."""
        can_move_right = True
        for block in self.curtetromino.blocks:
            xpos = self.curtetromino.pos[0] + block[0]
            ypos = self.curtetromino.pos[1] + block[1]
            if xpos >= self.ncols - 1:
                can_move_right = False
                break
            if self.dead_blocks[ypos][xpos + 1] is not None \
                    and xpos >= 0 and ypos >= 0 and ypos < self.nrows:
                can_move_right = False
                break

        if can_move_right:
            self.curtetromino.pos.x += 1

    def check_collisions(self):
        """Check collisions between the current (falling) tetromino with
        walls, ground and other tetrominos.
        """
        for block in self.curtetromino.blocks:
            xpos = self.curtetromino.pos[0] + block[0]
            ypos = self.curtetromino.pos[1] + block[1]
            if xpos < 0 or xpos >= self.ncols:
                return True
            if ypos + 1 >= self.nrows:
                return True
            if xpos >= 0 and xpos < self.ncols and \
               ypos >= 0 and ypos < self.nrows and \
               self.dead_blocks[ypos][xpos] is not None:
                return True
        return False

    def check_collision_below(self):
        """Check collisions between the current (falling) tetromino with
        ground and obstacles below.
        """
        for block in self.curtetromino.blocks:
            xpos = self.curtetromino.pos[0] + block[0]
            ypos = self.curtetromino.pos[1] + block[1]
            if ypos + 1 >= self.nrows:
                return True
            else:
                if self.dead_blocks[ypos+1][xpos] is not None and \
                        xpos >= 0 and xpos < self.ncols and \
                        ypos >= 0 and ypos < self.nrows:
                    return True
        return False

    def get_completed_rows(self):
        """Check for completely filled rows and assign points."""
        assert self.curtetromino is None
        completed_rows = []
        for i in xrange(self.nrows):
            num_dead_blocks = 0
            for j in xrange(self.ncols):
                if self.dead_blocks[i][j] is not None:
                    num_dead_blocks += 1
            if num_dead_blocks == self.ncols:
                completed_rows.append(i)
        return completed_rows

    def remove_rows(self, rows):
        """Remove all blocks in given rows."""
        for i in rows:
            for j in xrange(self.ncols):
                self.dead_blocks[i][j] = None
                if i > 0:
                    for k in xrange(i, -1, -1):
                        if k == 0:
                            self.dead_blocks[k][j] = None
                        else:
                            self.dead_blocks[k][j] = self.dead_blocks[k-1][j]

    def deposit_tetromino(self):
        """The tetromino piece has hit the ground and is converted
        to a dead block."""
        for block in self.curtetromino.blocks:
            ypos, xpos = self.curtetromino.pos.y + block[1], \
                         self.curtetromino.pos.x + block[0]
            self.dead_blocks[ypos][xpos] = self.curtetromino.color

        self.curtetromino = None

    def update(self):
        """Update tetromino piece and other blocks."""
        if self.curtetromino is None:
            self.spawn_tetromino()
            self.points += 1
        if not self.check_collision_below():
            self.curtetromino.pos.y += 1

        if self.check_collision_below():
            assert self.curtetromino is not None
            if self.is_game_over():
                self.reset()
            else:
                self.deposit_tetromino()
                completed_rows = self.get_completed_rows()
                self.points += calculate_points(len(completed_rows))
                self.remove_rows(completed_rows)

class TetrisWindow(tk.Frame):
# pylint: disable=R0904
# pylint: disable=too-many-instance-attributes
    """The main tetris window class! Runs the tetris game and updates
    tetrominos."""

    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.center_window()
        self.master = master

        self.game = Tetris(NUM_ROWS, NUM_COLS)
        self.time_step = TIME_STEP

        #pylint: disable=unused-variable
        self.rects = [[None for i in range(self.game.ncols)]
                            for j in range(self.game.nrows)]

        canvas_frame = tk.Frame(master, relief=tk.GROOVE, borderwidth=4,
                width=CANVAS_WIDTH + 6, height=CANVAS_HEIGHT + 6)
        self.canvas = tk.Canvas(canvas_frame, bg='white',
                width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.create_grid()
        self.canvas.pack(fill=tk.BOTH)
        canvas_frame.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)

        info_frame = tk.Frame(self, relief=tk.RAISED)

        points_frame = tk.Frame(info_frame, relief=tk.GROOVE, borderwidth=3)
        ptfont = tkFont.Font(family="Helvetica", size=14, weight="bold")
        plbl = tk.Label(points_frame, text='Points: ', font=ptfont)
        plbl.pack(side=tk.LEFT)
        self.score_str = tk.StringVar()
        points_lbl = tk.Label(points_frame, textvariable=self.score_str,
                justify=tk.RIGHT, width=4, font=ptfont)
        points_lbl.pack(side=tk.RIGHT)
        self.score_str.set("0")
        points_frame.pack(ipadx=5, ipady=5)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, pady=40)

        self.start_time = time.time()
        self.pause_on = False

    def center_window(self):
        """Set the window in the center of the screen."""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        xpos = (screen_width - SCREEN_WIDTH)/2
        ypos = (screen_height - SCREEN_HEIGHT)/2
        self.master.geometry('%dx%d+%d+%d' %
                (SCREEN_WIDTH, SCREEN_HEIGHT, xpos, ypos))

    def create_grid(self):
        """Create a matrix of rectangles."""
        offset = 0.02 * BOX_WIDTH
        for i in xrange(self.game.nrows):
            for j in xrange(self.game.ncols):
                self.rects[i][j] = self.canvas.create_rectangle(
                    j*BOX_WIDTH + offset + 1,
                    i*BOX_WIDTH + offset + 1,
                    (1 + j) * BOX_WIDTH - offset,
                    (1 + i) * BOX_WIDTH - offset,
                    fill='white', outline='#eeeeee'
                    )

    def run(self):
        """This is the main loop, call the update function."""
        self.after(self.time_step, self.update)

    def on_key_press(self, event):
        """Handle key-press events."""
        if event.char == 'p':
            self.pause_on = not self.pause_on
        elif event.char == 'q':
            self.master.quit()
        elif event.char == 's':
            self.save_state()
        elif event.char == 'l':
            self.load_state()
        elif self.game.curtetromino is not None and \
            not self.game.check_collision_below():
            if event.keysym == 'Right':
                self.game.move_right()
            elif event.keysym == 'Left':
                self.game.move_left()
            elif event.keysym == 'Up':
                blocks = self.game.curtetromino.blocks[:]
                rot = self.game.curtetromino.rotation
                self.game.curtetromino.rotate()
                if self.game.check_collisions():
                    self.game.curtetromino.blocks = blocks[:]
                    self.game.curtetromino.rotation = rot
            elif event.keysym == 'Down' and \
                    time.time() - self.start_time > KEYDOWN_WAIT_TIME:
                self.start_time = time.time()
                while not self.game.check_collision_below():
                    self.game.curtetromino.pos.y += 1
                    self.game.points += 1
                self.game.deposit_tetromino()
                self.game.points += calculate_points(
                    len(self.game.get_completed_rows())
                    )

            self.draw()

    def draw_grid(self):
        """Draw grid lines and fill with white color."""
        for i in xrange(self.game.nrows):
            for j in xrange(self.game.ncols):
                self.canvas.itemconfigure(
                    self.rects[i][j], fill='white', outline='#f8f8f8'
                    )

    def draw_blocks(self):
        """Draw all blocks, the dead ones and the current tetromino."""
        for i in xrange(self.game.nrows):
            for j in xrange(self.game.ncols):
                if self.game.dead_blocks[i][j] is not None:
                    self.canvas.itemconfigure(self.rects[i][j],
                        fill=self.game.dead_blocks[i][j], outline='black')

        if self.game.curtetromino is not None:
            for block in self.game.curtetromino.blocks:
                xpos = self.game.curtetromino.pos[0] + block[0]
                ypos = self.game.curtetromino.pos[1] + block[1]
                if not (xpos < 0 or xpos >= self.game.ncols
                     or ypos < 0 or ypos >= self.game.nrows):
                    self.canvas.itemconfigure(self.rects[ypos][xpos],
                        fill=self.game.curtetromino.color, outline='black'
                        )

    def draw(self):
        """Draw canvas."""
        self.draw_grid()
        self.draw_blocks()

    def update(self):
        """Update tetromino piece and game time."""
        if not self.pause_on:
            self.game.update()
            self.draw()

        self.time_step *= TIME_STEP_REDUCE
        if self.time_step < 10:
            self.time_step = 10
        self.score_str.set(str(self.game.points))
        self.after(int(self.time_step), self.update)

    def save_state(self):
        """Save the current (complete) state of the game."""
        np.savez(SAVED_STATE_NAME, curtetromino=[self.game.curtetromino],
                blocks=self.game.dead_blocks, points=[self.game.points])

    def load_state(self):
        """Load previous saved game state."""
        npzfile = np.load(SAVED_STATE_NAME + '.npz')
        self.game.curtetromino = npzfile['curtetromino'][0]
        self.game.dead_blocks = npzfile['blocks']
        self.game.points = npzfile['points'][0]

def main():
    """Starting the main game. Create the Tetris window."""
    root = tk.Tk()
    root.title('Tetris')
    root.resizable(0, 0)
    game = TetrisWindow(root)
    root.bind("<Key>", game.on_key_press)
    game.pack()
    game.run()
    root.mainloop()

if __name__ == '__main__':
    main()
