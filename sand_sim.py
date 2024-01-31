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
rect_coords = [] # keeps track of where the sand is


# \--- CODE SIMPLIFICATION FUNCTIONS ---/
# -> Enhance code clarity and streamlining through functions <-


"""
-> Returns the index of the given coordinates (x, y) in the rect_coords list <-

    Parameters:
    - x (int): The x-coordinate.
    - y (int): The y-coordinate.

    Returns:
    - int: The index of the coordinates in the rect_coords list.
"""
def index(x, y):
    for i, (col, row) in enumerate(rect_coords):
        if col == x and row == y:
            return i

"""

-> Move a cell in the grid to a new position <-

Args:
    col (int): The column index of the cell to be moved.
    row (int): The row index of the cell to be moved.
    new_col (int): The new column index for the cell.

"""
def cellMovement(col, row, new_col):
    grid[col, row] = 0
    del rect_coords[index(col, row)]
    grid[new_col, row+1] = 1
    rect_coords.append((new_col, row+1))

column_order = list(range(cols))
def randomShuffle():
    random.shuffle(column_order)

def randomChoice(values):
    return random.choice(values)

"""

-> Decorator that limits the rate at which a function can be invoked <-

"""
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


"""

-> Moves the sand particles in the grid <-

    -> This method iterates through each column in a random order and simulates the falling movement of the sand particles.
    -> The sand particles fall down one row at a time, and if there is an empty cell below, the sand particle moves to that cell.
    -> If the cell below has sand and the diagonal is empty, the sand particle may randomly move to the left or right (depending on which is available).

    Note:
        - The order of processing the columns is randomized to create a more symmetrical falling movement.
        - The sand particles are represented by the value 1 in the grid.
        - The grid is a two-dimensional array.

"""
def moveSand():
    col_thread = threading.Thread(target=randomShuffle, args=())
    col_thread.start()
    col_thread.join()
    for i in column_order:
        for j in range(rows-1, -1, -1): # The second value is -1 so the top row is included in the sand spawnable area
            if j+1 <= rows-1:
                below = grid[i, j+1];
                if grid[i, j] == 1:
                    if below == 0: # Checking if there's already sand below
                        cellMovement(i, j, i)
                    else:
                        rand = randomChoice([-1, 1])

                        belowA = grid[i+rand, j+1] if i+rand in range(cols) else 1
                        belowB = grid[i-rand, j+1] if i-rand in range(cols) else 1
                        if belowA == 0:
                            cellMovement(i, j, i+rand)
                        elif belowB == 0:
                            cellMovement(i, j, i-rand)


"""

-> Draws the sand on the screen <-

    -> This function calls the moveSand() function to update the sand positions,
    and then draws each sand rectangle on the screen using pygame's draw.rect() function.
    -> Also by iterating through the rect_coords list (which keeps track of the occupied cells)
    there's an increase in performance due to optimizing the search process and minimizing redundant computations

"""
def drawSand():
    moveSand()
    for _, (x, y) in enumerate(rect_coords):
        pg.draw.rect(screen, white, ((x * cell_size, y * cell_size), (cell_size, cell_size)))


"""

-> Spawns sand particles on the grid based on the mouse position <-

    -> The sand particles are created within a specific radius around the mouse position,
    and if a cell, within the radius, is empty, a sand particle is created in it.

"""
@rate_limit(interval=0.05)
def summonSand():
    sand_radius = cell_size // 2
    mouse_state = pg.mouse.get_pressed()
    if mouse_state[0]:
        mouseX, mouseY = pg.mouse.get_pos()
        for i in range(-sand_radius, sand_radius, 1):
            for j in range(-sand_radius, sand_radius, 1):
                if randomChoice([True, False]):
                    col = (mouseX // cell_size) + i
                    row = (mouseY // cell_size) + j
                    if col in range(cols) and row in range(rows):
                        if grid[col, row] == 0:
                            grid[col, row] = 1
                            rect_coords.append((col, row))



# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(black)
    summonSand()
    drawSand()
    pg.display.flip()
    clock.tick(60)
