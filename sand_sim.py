import pygame as pg
import time
import random
from pygame.locals import *

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
cell_size = 10
cols = screenW // cell_size
rows = screenH // cell_size
grid = [[0 for _ in range(cols)] for _ in range(rows)]
prev_grid = [[0 for _ in range(cols)] for _ in range(rows)]



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


def moveSand():
    # this method makes the columns be processed in a random order making the falling movement more symmetrical
    column_order = list(range(cols))
    random.shuffle(column_order)
    for i in column_order: # the previous method (for i in range(cols)) made the sand, when falling to the right, "spawn" in place and gave the effect of rising up
        for j in range(rows-1, -1, -1): # if the end value is 0 the topmost row is not "considered" for the sand to spawn
            if j+1 <= rows-1:
                below = grid[i][j+1];
                if grid[i][j] == 1:
                    if below == 0:
                        grid[i][j] = 0
                        grid[i][j+1] = 1
                    else:
                        # To make the sand pile up more naturally, a little bit of randomness helps :)
                        rand = random.choice([-1, 1])

                        belowA = grid[i+rand][j+1] if i + rand in range(cols) else 1
                        belowB = grid[i-rand][j+1] if i-rand in range(cols) else 1
                        if belowA == 0:
                            grid[i][j] = 0
                            grid[i+rand][j+1] = 1
                        elif belowB == 0:
                            grid[i][j] = 0
                            grid[i-rand][j+1] = 1


def drawSand():
    moveSand()
    for i in range(cols):
        for j in range(rows):
            if grid[i][j] > 0:
                pg.draw.rect(screen, white, ((i * cell_size, j * cell_size), (cell_size, cell_size)))


@rate_limit(interval=0.05)
# Creating Sand by pressing the mouse
def mouseSand():
    # Sand spawning area
    radius = random.randint(5, 8)
    sand_radius = radius // 2
    mouse_state = pg.mouse.get_pressed()
    if mouse_state[0]:
        mouseX, mouseY = pg.mouse.get_pos()
        for i in range(-sand_radius, sand_radius, 1):
            for j in range(-sand_radius, sand_radius, 1):
                if random.choice([True, False]):
                    col = (mouseX // cell_size) + i
                    row = (mouseY // cell_size) + j
                    if col in range(cols) and row in range(rows): # checks if the mouse is inside the window 
                        if grid[col][row] == 0: # prevents summoning sand inside cells that already has it
                            grid[col][row] = 1


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
    clock.tick(45)
