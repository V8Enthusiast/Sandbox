import pygame
import random

class WaterParticle:
    def __init__(self, simulation, x, y, color):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = color
        self.rendered = False

    def render(self):
        if self.rendered is False:
            rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
            rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
            pygame.draw.rect(self.simulation.window, self.color, rect)
            self.calculate_physics()
            self.rendered = True

    def calculate_physics(self):
        if self.y + 1 < self.simulation.ROWS:
            #print(self.simulation.map[self.y + 1][self.x])
            pass
        #print(self.simulation.LIQUIDS)
        if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] in self.simulation.LIQUIDS: # particle under is a moving one (sand)
            # #print("f")
            # if self.x + 1 < self.simulation.COLUMNS:
            #     right_below = self.simulation.map[self.y + 1][self.x + 1] in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS + self.simulation.LIQUIDS # checks if the particle should move down to the right
            # else:
            #     right_below = True
            # if self.x - 1 >= 0:
            #     left_below = self.simulation.map[self.y + 1][self.x - 1] in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS + self.simulation.LIQUIDS # checks if the particle should move down to the left
            # else:
            #     left_below = True
            #
            # if right_below is False and left_below is False: # if both are true choose one side which the particle will head to
            #     if random.randint(0, 100) >= 50:
            #         left_below = True
            #     else:
            #         right_below = True
            #
            # if right_below is False: # particle falls to the right
            #     self.simulation.map[self.y][self.x] = 0  # reset the current square
            #     self.simulation.map[self.y + 1][self.x + 1] = 1  # add the water back 1 square lower
            #     self.simulation.particles[(self.x, self.y)] = None
            #     self.simulation.particles[(self.x + 1, self.y + 1)] = self
            #     self.y += 1
            #     self.x += 1
            #     print("right")
            #
            # if left_below is False: # particle falls to the left
            #     self.simulation.map[self.y][self.x] = 0  # reset the current square
            #     self.simulation.map[self.y + 1][self.x - 1] = 1  # add the water back 1 square lower
            #     self.simulation.particles[(self.x, self.y)] = None
            #     self.simulation.particles[(self.x - 1, self.y + 1)] = self
            #     self.y += 1
            #     self.x -= 1
            #     print("left")

            # to the right
            first_empty_particle_right_x = None
            for i in range(self.simulation.COLUMNS - self.x):
                if self.simulation.map[self.y + 1][self.x + i] == 0:
                    first_empty_particle_right_x = self.x + i
                    break
                if self.simulation.map[self.y + 1][self.x + i] in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS:
                    break

            # to the left
            first_empty_particle_left_x = None
            for n in range(self.x):
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

        elif self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] not in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS: # check if there is a solid object or border under the sand
            self.simulation.map[self.y][self.x] = 0 # reset the current square
            self.simulation.map[self.y + 1][self.x] = 2 # add the sand back 1 square lower
            self.simulation.particles[(self.x, self.y)] = None
            self.simulation.particles[(self.x, self.y + 1)] = self
            self.y += 1
