import pygame as pg
from pygame.locals import *
import time
import random
import numpy as np

from particle import Particle

pg.init()

# Setup
screenW = 600
screenH = 600

screen = pg.display.set_mode((screenW, screenH))
clock = pg.time.Clock()

FPS = 30

bg_color = (85, 35, 65)
black = (0, 0, 0)
sand_color = (255, 253, 150)
white = (255, 255, 255, 128)

# Grid
cell_size = 5
cols = screenW // cell_size
rows = screenH // cell_size
grid = np.zeros((cols, rows), dtype=int)
rect_coords = [] # Keeps track of where there are sand particles

gravity = 0.5


mouse_radius = 20
surface = pg.Surface((20, 20), pg.SRCALPHA)

def mousePos():
    return pg.mouse.get_pos()

def mouseState():
    return pg.mouse.get_pressed()

def drawMouseRadius():
    mouseX, mouseY = mousePos()

    pg.draw.rect(surface, white, pg.Rect(0, 0, mouse_radius, mouse_radius), 2)
    screen.blit(surface, (mouseX - mouse_radius//2, mouseY - mouse_radius//2))



"""

-> Moves the sand particles in the grid based on gravity <-

    -> This function iterates over the `rect_coords` list and calls the `move` method on each sand particle.
    The `move` method takes the `grid`, `gravity`, `cols`, and `rows` as parameters.

"""
def moveSand():
    for index in range(len(rect_coords)):
        rect_coords[index].move(grid, gravity, cols, rows)

"""

-> Draws the sand on the screen <-

    -> This function calls the moveSand() function to update the sand positions,
    and then draws each sand rectangle on the batch_surface using pygame's draw.rect() function
    and blits it to the screen to save on performance.
    -> Also by iterating through the rect_coords list (which keeps track of the occupied cells)
    there's an increase in performance due to optimizing the search process and minimizing redundant computations

"""
def drawSand():
    moveSand()

    # create a new surface for batch rendering
    batch_surface = pg.Surface((screenW, screenH))
    # by using convert on the surface it can make the blitting faster
    batch_surface = batch_surface.convert()

    for particle in rect_coords:
        x, y = particle.position
        pg.draw.rect(batch_surface, sand_color, ((x * cell_size, y * cell_size), (cell_size, cell_size)))

    # draw the surface onto the screen
    screen.blit(batch_surface, (0,0))

"""

-> Spawns sand particles on the screen based on the mouse position and radius <-

    -> The sand particles are created within a specific radius around the mouse position,
    and if a cell, within the radius, is empty, a sand particle is created in it.

"""
def summonSand():
    if mouseState()[0]:
        sand_radius = 3

        mouseX, mouseY = mousePos()
        cellX, cellY = (mouseX // cell_size), (mouseY // cell_size)
        for i in range(-sand_radius, sand_radius, 1):
            for j in range(-sand_radius, sand_radius, 1):
                if random.choice([True, False]):
                    col = cellX + i
                    row = cellY + j
                    if col in range(cols) and row in range(rows):
                        if grid[col, row] == 0:
                            grid[col, row] = 1 # setting the cell state to 1
                            rect_coords.append(Particle(col, row)) # tracking the current coordinate of the summoned particle

"""

-> Erases sand particles on the screen based on the mouse position and radius <-

"""
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
                        for particle in rect_coords:
                            if particle.position == [col, row]:
                                rect_coords.remove(particle)
                                break


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
        pg.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
