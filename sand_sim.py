import pygame as pg
from pygame.locals import *
import time
import random
import numpy as np

pg.init()

# Setup
screenW = 600
screenH = 600

screen = pg.display.set_mode((screenW, screenH))
clock = pg.time.Clock()

bg_color = (85, 35, 65)
black = (0, 0, 0)
sand = (255, 253, 150)
white = (255, 255, 255, 128)

# Grid
cell_size = 5
cols = screenW // cell_size
rows = screenH // cell_size
grid = np.zeros((cols, rows), dtype=int)
rect_coords = [] # Keeps track of where there are sand particles


def mousePos():
    return pg.mouse.get_pos()

def mouseState():
    return pg.mouse.get_pressed()


"""

-> Move a cell in the grid to a new position <-

    Note:
        - The grid is a two-dimensional array.

    Args:
        col (int): The column index of the cell to be moved.
        row (int): The row index of the cell to be moved.
        new_col (int): The new column index for the cell.

"""
def cellMovement(col, row, new_col):
    grid[col, row] = 0
    del rect_coords[rect_coords.index((col, row))]
    grid[new_col, row+1] = 1
    rect_coords.append((new_col, row+1))

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

    -> This method iterates through the coordinates of the sand particles in the grid and checks if there is sand below each one. 
    -> The sand particles fall down one row at a time, and if there is an empty cell below, the sand particle moves to that cell.
    -> If the cell below has sand and the diagonal is empty, the sand particle may randomly move to the left or right (depending on which is available).

    Note:
        - The sand particles are represented by the value 1 in the grid.
        - rect_coords is a list containing tuples representing the coordinates of particles in the format (column, row).

"""
def moveSand():
    for i, j in rect_coords:
        if grid[i, j] == 1:
            if j+1 <= rows-1:
                below = grid[i, j+1];
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


def drawMouseRadius():
    radius = 20
    mouseX, mouseY = mousePos()

    surface = pg.Surface((20, 20), pg.SRCALPHA)
    pg.draw.rect(surface, white, pg.Rect(0, 0, radius, radius), 2)
    screen.blit(surface, (mouseX - radius//2, mouseY - radius//2))


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
        pg.draw.rect(screen, sand, ((x * cell_size, y * cell_size), (cell_size, cell_size)))

"""

-> Spawns sand particles on the grid based on the mouse position <-

    -> The sand particles are created within a specific radius around the mouse position,
    and if a cell, within the radius, is empty, a sand particle is created in it.

    Note:
        - 

"""
@rate_limit(interval=0.05) # the bigger the interval the less frequency the sand will spawn
def summonSand():
    if mouseState()[0]:

        # The numbers should be around the cell_size value (5), to give an extra flailing/flaming effect without exagerating
        # Assigning 1 creates a reminiscent feel of a dying flame rekindling
        # Opt for odd numbers to avoid redundancy; even numbers yield the same result due to floor division "//" halving them
        # radius = randomChoice([3, 5, 7, 9])
        sand_radius = 2

        mouseX, mouseY = mousePos()
        cellX, cellY = (mouseX // cell_size), (mouseY // cell_size)
        for i in range(-sand_radius, sand_radius, 1):
            for j in range(-sand_radius, sand_radius, 1):
                if randomChoice([True, False]):
                    col = cellX + i
                    row = cellY + j
                    if col in range(cols) and row in range(rows):
                        if grid[col, row] == 0:
                            grid[col, row] = 1 # setting the cell state to 1
                            rect_coords.append((col, row)) # tracking the current coordinate of the summoned particle

def eraseSand():
    if mouseState()[2]:
        erase_radius = 2
        mouseX, mouseY = mousePos()
        cellX, cellY = (mouseX // cell_size), (mouseY // cell_size)
        for i in range(-erase_radius, erase_radius, 1):
            for j in range(-erase_radius, erase_radius, 1):
                col = cellX + i
                row = cellY + j
                if col in range(cols) and row in range(rows):
                    if grid[col, row] == 1:
                        grid[col, row] = 0
                        del rect_coords[rect_coords.index((col, row))]



# Main loop
def main():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False

        screen.fill(black)
        summonSand()
        eraseSand()
        drawSand()
        drawMouseRadius()
        pg.display.flip()
        clock.tick(45)

if __name__ == "__main__":
    main()
