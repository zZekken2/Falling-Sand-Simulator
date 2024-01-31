import pygame as pg
from pygame.locals import *
import time
import random
import numpy as np
import threading

pg.init()

# Setup
screenW = 600
screenH = 600

screen = pg.display.set_mode((screenW, screenH))
clock = pg.time.Clock()

bg_color = (85, 35, 65)
black = (0, 0, 0)
white = (255, 255, 255)

# Grid
cell_size = 5
cols = screenW // cell_size
rows = screenH // cell_size
grid = np.zeros((cols, rows), dtype=int)



def rate_limit(interval):
    def decorator(func):
        last_invocation = 0

        def wrapper(*args, **kwargs):
            nonlocal last_invocation
            elapsed = time.time() - last_invocation
            if elapsed >= interval:
                last_invocation = time.time()
                return func(*args, **kwargs)
        return wrapper
    return decorator


def cellMovement(col, row, new_col):
    grid[col, row] = 0
    grid[new_col, row+1] = 1


column_order = list(range(cols))
def randomShuffle():
    random.shuffle(column_order)


def randomChoice(values):
    return random.choice(values)


def moveSand():
    # this method makes the columns be processed in a random order making the falling movement more symmetrical
    col_thread = threading.Thread(target=randomShuffle, args=())
    col_thread.start()
    col_thread.join()
    for i in column_order: # the previous method (for i in range(cols)) made the sand, when falling to the right, "spawn" in place and gave the effect of rising up
        for j in range(rows-1, -1, -1): # if the end value is 0 the topmost row is not "considered" for the sand to spawn
            if j+1 <= rows-1:
                below = grid[i, j+1];
                if grid[i, j] == 1:
                    if below == 0:
                        cellMovement(i, j, i)
                    else:
                        # To make the sand pile up more naturally, a little bit of randomness helps :)
                        rand = randomChoice([-1, 1])

                        belowA = grid[i+rand, j+1] if i+rand in range(cols) else 1
                        belowB = grid[i-rand, j+1] if i-rand in range(cols) else 1
                        if belowA == 0:
                            cellMovement(i, j, i+rand)
                        elif belowB == 0:
                            cellMovement(i, j, i-rand)


def drawSand():
    moveSand()
    for i in range(cols):
        for j in range(rows):
            if grid[i, j] > 0:
                pg.draw.rect(screen, white, ((i * cell_size, j * cell_size), (cell_size, cell_size)))


@rate_limit(interval=0.05)
# Creating Sand by pressing the mouse
def mouseSand():
    # Sand spawning area
    sand_radius = cell_size // 2
    mouse_state = pg.mouse.get_pressed()
    if mouse_state[0]:
        mouseX, mouseY = pg.mouse.get_pos()
        for i in range(-sand_radius, sand_radius, 1):
            for j in range(-sand_radius, sand_radius, 1):
                if randomChoice([True, False]):
                    col = (mouseX // cell_size) + i
                    row = (mouseY // cell_size) + j
                    if col in range(cols) and row in range(rows): # checks if the mouse is inside the window 
                        if grid[col, row] == 0: # prevents summoning sand inside cells that already has it
                            grid[col, row] = 1


# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(black)
    mouseSand()
    drawSand()
    pg.display.flip()
    clock.tick(60)
