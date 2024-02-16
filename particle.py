import random

class Particle:
    def __init__(self, col, row):
        self.position = [col, row]
        self.velocity = 0

        self.side_drift = False # 

    def applyGravity(self, force):
        self.velocity += force

    """
    -> Find the last empty cell in a column of the grid <-

        Parameters:
            grid (numpy.ndarray): The grid representing the sand simulation.
            rows (int): The number of rows in the grid.

        Returns:
            int: The index of the last empty cell in the column.
    """
    def lastCell(self, grid, rows):
        for i in range(rows-1, self.position[1], -1):
            if grid[self.position[0], i] == 0:
                return i
        return self.position[1]

    """
    -> Moves the particle on the grid based on the given force and grid dimensions <-

        Parameters:
        - grid (numpy.ndarray): The grid representing the sand simulation.
        - force (float): The force of gravity applied to the particle.
        - cols (int): The number of columns in the grid.
        - rows (int): The number of rows in the grid.
    """
    def move(self, grid, force, cols, rows):
        col = self.position[0]
        row = self.position[1]
        grid[col, row] = 0

        if not self.side_drift:
            next_row = row + self.velocity
            last_cell = self.lastCell(grid, rows)

            if next_row < last_cell:
                self.applyGravity(force)
                self.position[1] += int(self.velocity)
            else:
                self.position[1] = last_cell
                self.side_drift = True
        else:
            rand = random.choice([-1, 1])

            belowA = grid[col+rand, row+1] if col+rand in range(cols) and row+1 in range(rows) else 1
            belowB = grid[col-rand, row+1] if col-rand in range(cols) and row+1 in range(rows) else 1

            if belowA == 0:
                self.position[0] += rand
                self.position[1] += 1
            elif belowB == 0:
                self.position[0] -= rand
                self.position[1] += 1

        grid[self.position[0], self.position[1]] = 1
