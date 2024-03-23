import pygame
import random

class WaterParticle:
    def __init__(self, simulation, x, y, color):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = color
        self.rendered = False
        self.isFalling = True

    def render(self):
        if self.rendered is False:
            rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
            rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
            pygame.draw.rect(self.simulation.window, self.color, rect)
            self.calculate_physics()
            self.rendered = True

    def calculate_physics(self):
        if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] != 0 and self.simulation.particles[(self.x, self.y + 1)].isFalling is False:
            self.isFalling = False
        elif self.y + 1 >= self.simulation.ROWS:
            self.isFalling = False

        if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] == 0:
            self.isFalling = True

        if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] != 0 and self.isFalling is False: # particle under is a not air

            # to the right
            first_empty_particle_right_x = None
            for i in range(1, self.simulation.COLUMNS - self.x):
                if self.simulation.map[self.y + 1][self.x + i] == 0:
                    first_empty_particle_right_x = self.x + i
                    break
                if self.simulation.map[self.y + 1][self.x + i] in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS:
                    break

            # to the left
            first_empty_particle_left_x = None
            for n in range(1, self.x):
                if self.simulation.map[self.y + 1][self.x - n] == 0:
                    first_empty_particle_left_x = self.x - n
                    break
                if self.simulation.map[self.y + 1][self.x - n] in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS:
                    break

            if first_empty_particle_left_x is not None and first_empty_particle_right_x is not None: # if water can flow to both sides choose only one
                if abs(self.x - first_empty_particle_left_x) == abs(self.x - first_empty_particle_right_x):
                    if random.randint(0, 100) >= 50:
                        first_empty_particle_left_x = None
                    else:
                        first_empty_particle_right_x = None
                else:
                    if abs(self.x - first_empty_particle_left_x) < abs(self.x - first_empty_particle_right_x): # left is closer
                        first_empty_particle_right_x = None
                    else:
                        first_empty_particle_left_x = None

            if first_empty_particle_left_x is not None:
                self.simulation.map[self.y][self.x] = 0  # reset the current square
                self.simulation.map[self.y + 1][first_empty_particle_left_x] = 2  # add the water to the chosen square
                self.simulation.particles[(self.x, self.y)] = None
                self.simulation.particles[(first_empty_particle_left_x, self.y + 1)] = self
                self.y += 1
                self.x = first_empty_particle_left_x

            if first_empty_particle_right_x is not None:
                self.simulation.map[self.y][self.x] = 0  # reset the current square
                self.simulation.map[self.y + 1][first_empty_particle_right_x] = 2  # add the water to the chosen square
                self.simulation.particles[(self.x, self.y)] = None
                self.simulation.particles[(first_empty_particle_right_x, self.y + 1)] = self
                self.y += 1
                self.x = first_empty_particle_right_x

        elif self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] not in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS + self.simulation.LIQUIDS: # water is on top of air
            self.simulation.map[self.y][self.x] = 0 # reset the current square
            self.simulation.map[self.y + 1][self.x] = 2 # add the sand back 1 square lower
            self.simulation.particles[(self.x, self.y)] = None
            self.simulation.particles[(self.x, self.y + 1)] = self
            self.y += 1