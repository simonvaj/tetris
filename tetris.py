import Tkinter as tk
import tkFont
import random
import time
import numpy as np
from utils import *
from tetromino import *

dt = DEFAULT_TIME_STEP
        
class Tetris(tk.Frame):

    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.center_window()
        self.master = master
        self.nrows = NUM_ROWS
        self.ncols = NUM_COLS
        self.rects = [[None for i in range(self.ncols)] for j in range(self.nrows)]
        self.curtetromino = None
        self.iters = 0
        
        canvas_frame = tk.Frame(master, relief=tk.GROOVE, borderwidth=4, width=CANVAS_WIDTH + 6, height=CANVAS_HEIGHT + 6)
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.create_grid()
        self.canvas.pack(fill=tk.BOTH)
        canvas_frame.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)
        
        info_frame = tk.Frame(self, relief=tk.RAISED)
        
        points_frame = tk.Frame(info_frame, relief=tk.GROOVE, borderwidth=3)
        ptfont = tkFont.Font(family="Helvetica", size=14, weight="bold")
        plbl = tk.Label(points_frame, text='Points: ', font=ptfont)
        plbl.pack(side=tk.LEFT)
        self.npts_str = tk.StringVar()
        points_lbl = tk.Label(points_frame, textvariable=self.npts_str, justify=tk.RIGHT, 
                              width=4, font=ptfont)
        points_lbl.pack(side=tk.RIGHT)
        self.npts_str.set("0")
        points_frame.pack(ipadx=5, ipady=5)
        info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, pady=40)
  
        self.iters = 0
        self.loop = 0
        self.dead_blocks = [[None for i in xrange(self.ncols)] for j in xrange(self.nrows)]
        self.dt = DEFAULT_TIME_STEP
        
        self.keydown_wait_time = 0.5
        self.start_time = time.time()
        
        self.pause_on = False
        
        self.points = 0
        self.level = 0

    def center_window(self):
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
          
        x = (sw - SCREEN_WIDTH)/2
        y = (sh - SCREEN_HEIGHT)/2
        self.master.geometry('%dx%d+%d+%d' % (SCREEN_WIDTH, SCREEN_HEIGHT, x, y))
        
    def run(self):
        self.after(dt, self.update) 
    
    def create_grid(self):
        OFFSET = 0.02 * BOX_WIDTH
        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                self.rects[i][j] = self.canvas.create_rectangle(j*BOX_WIDTH + OFFSET + 1, 
                                                                i*BOX_WIDTH + OFFSET + 1,
                                                                (1 + j) * BOX_WIDTH - OFFSET, 
                                                                (1 + i) * BOX_WIDTH - OFFSET,
                                                                fill='white', outline='#eeeeee')
    def draw_grid(self):
        OFFSET = 0.02 * BOX_WIDTH
        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                self.canvas.itemconfigure(self.rects[i][j], fill='white', outline='#f8f8f8')
                                                                
    def reset(self):
        self.points = 0
        self.curtetromino = None
        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                self.dead_blocks[i][j] = None
    
    def spawn_tetromino(self):
    
        r = random.randint(0, 6)
        if r == 0:
            self.curtetromino = SquareTetromino()
        elif r == 1:
            self.curtetromino = StraightTetromino()
        elif r == 2:
            self.curtetromino = TTetromino()
        elif r == 3:
            self.curtetromino = JTetromino()
        elif r == 4:
            self.curtetromino = LTetromino()
        elif r == 5:
            self.curtetromino = STetromino()
        elif r == 6:
            self.curtetromino = ZTetromino()
        
    def is_game_over(self):
        for x in xrange(self.ncols):
            if self.dead_blocks[0][x] is not None:
                return True
        return False
                            
    def move_left(self):
        can_move_left = True
        for block in self.curtetromino.blocks:
            x, y = self.curtetromino.pos[0] + block[0], self.curtetromino.pos[1] + block[1]
            if x <= 0:
                can_move_left = False
                break
                
            if self.dead_blocks[y][x - 1] is not None and x >= 1 and x < self.ncols and y >= 0 and y < self.nrows:
                can_move_left = False
                break

        if can_move_left:
            self.curtetromino.pos.x -= 1
                   
    def move_right(self):
        can_move_right = True
        for block in self.curtetromino.blocks:
            x, y = self.curtetromino.pos[0] + block[0], self.curtetromino.pos[1] + block[1]
            if x >= self.ncols - 1:
                can_move_right = False
                break
            if self.dead_blocks[y][x + 1] is not None and x >= 0 and y >= 0 and y < self.nrows:
                can_move_right = False
                break

        if can_move_right:
            self.curtetromino.pos.x += 1

    def check_collisions(self):
        """
        Check collisions between the current (falling) tetromino with 
        walls, ground and other tetrominoes.
        """
        for block in self.curtetromino.blocks:
            x, y = self.curtetromino.pos[0] + block[0], self.curtetromino.pos[1] + block[1]
            if x < 0 or x >= self.ncols:
                return True
            if y + 1 >= self.nrows:
                return True
            if x >= 0 and x < self.ncols and y >= 0 and y < self.nrows and self.dead_blocks[y][x] is not None:
                return True
        return False
    
    def check_collision_below(self):
        """
        Check collisions between the current (falling) tetromino with 
        ground and obstacles below.
        """
        for block in self.curtetromino.blocks:
            x, y = self.curtetromino.pos[0] + block[0], self.curtetromino.pos[1] + block[1]
            if y + 1 >= self.nrows:
                return True
            else:
                if self.dead_blocks[y+1][x] is not None and x >= 0 and x < self.ncols and \
                   y >= 0 and y < self.nrows:
                    return True
        return False
        
    def check_rows(self):
        assert self.curtetromino is None
        complete_rows = []
        for i in xrange(self.nrows):
            num_dead_blocks = 0
            for j in xrange(self.ncols):
                if self.dead_blocks[i][j] is not None:
                    num_dead_blocks += 1
            if num_dead_blocks == self.ncols:
                complete_rows.append(i)
               
        if len(complete_rows) == 1:
            self.points += 200
        elif len(complete_rows) == 2:
            self.points += 500
        elif len(complete_rows) == 3:
            self.points += 1100
        elif len(complete_rows) >= 4:
            self.points += 2000
            
        for i in complete_rows:
            for j in xrange(self.ncols):
                self.dead_blocks[i][j] = None
                if i > 0:
                    for k in xrange(i, -1, -1):
                        if k == 0:
                            self.dead_blocks[k][j] = None
                        else:
                            self.dead_blocks[k][j] = self.dead_blocks[k-1][j]
        
    def on_key_press(self, event):
    
        if event.char == 'p':
            self.pause_on = not self.pause_on
        elif event.char == 'q':
            self.master.quit()
        elif event.char == 's':
            self.save_state()
        elif event.char == 'l':
            self.load_state()
        elif self.curtetromino is not None and not self.check_collision_below():
            if event.keysym == 'Right':
                self.move_right()
            elif event.keysym == 'Left':
                self.move_left()
            elif event.keysym == 'Up':
                blocks = self.curtetromino.blocks[:]
                rot = self.curtetromino.rotation
                self.curtetromino.rotate()
                if self.check_collisions():
                    self.curtetromino.blocks = blocks[:]
                    self.curtetromino.rotation = rot
            elif event.keysym == 'Down' and time.time() - self.start_time > self.keydown_wait_time:
                self.start_time = time.time()
                while not self.check_collision_below():
                    self.curtetromino.pos.y += 1
                    self.points += 1
                self.deposit_tetromino()
                self.check_rows()

            self.draw()
        
        
    def draw(self):
        self.draw_grid()
        for i in xrange(self.nrows):
            for j in xrange(self.ncols):
                if self.dead_blocks[i][j] is not None:
                    self.canvas.itemconfigure(self.rects[i][j], fill=self.dead_blocks[i][j], outline='black')
        if self.curtetromino is not None:
            for b in self.curtetromino.blocks:
                y, x = self.curtetromino.pos[1] + b[1], self.curtetromino.pos[0] + b[0]
                if not (x < 0 or x >= self.ncols or y < 0 or y >= self.nrows):
                    self.canvas.itemconfigure(self.rects[y][x], fill=self.curtetromino.color, outline='black')

    def deposit_tetromino(self):
        for b in self.curtetromino.blocks:
            y, x = self.curtetromino.pos.y + b[1], self.curtetromino.pos.x + b[0]
            self.dead_blocks[y][x] = self.curtetromino.color
            
        self.curtetromino = None
        
    def update(self):
        
        if not self.pause_on:
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
                    self.check_rows()
            self.draw()
        
        self.dt *= TIME_STEP_REDUCE
        if self.dt < 10: self.dt = 10
        self.npts_str.set(str(self.points))
        self.after(int(self.dt), self.update)
    
    def save_state(self):
        np.savez(SAVED_STATE_NAME, curtetromino=[self.curtetromino], blocks=self.dead_blocks, points=[self.points])
        
    def load_state(self):
        npzfile = np.load(SAVED_STATE_NAME + '.npz')
        self.curtetromino = npzfile['curtetromino'][0]
        self.dead_blocks = npzfile['blocks']
        self.points = npzfile['points'][0]
    
def main():
    root = tk.Tk()
    root.title('Tetris')
    root.resizable(0, 0)
    game = Tetris(root)
    root.bind("<Key>", game.on_key_press)
    game.pack()    
    game.run()
    root.mainloop()
    
if __name__ == '__main__':
    main()
