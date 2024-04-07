import pygame
import random
colors = [(158, 158, 158), (169, 169, 169), (77, 77, 77)]
class SmokeParticle:
    def __init__(self, simulation, x, y):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = random.choice(colors)
        self.rendered = False
        self.isFalling = True
    def render(self):
        if self.rendered is False:
            rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
            rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
            pygame.draw.rect(self.simulation.window, self.color, rect)
            self.calculate_physics()
            self.rendered = True
            #self.color = random.choice(colors)

    def calculate_physics(self):
        if self.y - 1 >= 0 and self.simulation.smoke_map[self.y - 1][self.x] != 0 and self.simulation.smoke_particles[(self.x, self.y - 1)].isFalling is False:
            self.isFalling = False
        elif self.y - 1 < 0:
            self.isFalling = False

        if self.y - 1 >= 0 and self.simulation.smoke_map[self.y - 1][self.x] == 0:
            self.isFalling = True

        if self.y - 1 >= 0 and self.simulation.smoke_map[self.y - 1][self.x] == 1 and self.isFalling is False: # particle under is a moving one (sand)
            if self.x + 1 < self.simulation.COLUMNS:
                    right_below = self.simulation.smoke_map[self.y - 1][self.x + 1] == 1  # checks if the particle should move down to the right
            else:
                right_below = True
            if self.x - 1 >= 0:
                    left_below = self.simulation.smoke_map[self.y - 1][self.x - 1] == 1 # checks if the particle should move down to the left
            else:
                left_below = True


            if right_below is False and left_below is False: # if both are true choose one side which the particle will head to
                if random.randint(0, 100) >= 50:
                    left_below = True
                else:
                    right_below = True

            if right_below is False: # particle falls to the right
                self.simulation.smoke_map[self.y - 1][self.x + 1], self.simulation.smoke_map[self.y][self.x] = 1, self.simulation.smoke_map[self.y - 1][self.x + 1] # swap particles on the map
                self.simulation.smoke_particles[(self.x + 1, self.y - 1)], self.simulation.smoke_particles[(self.x, self.y)] = self, self.simulation.smoke_particles[(self.x + 1, self.y - 1)]
                if self.simulation.smoke_particles[(self.x, self.y)] is not None:
                    self.simulation.smoke_particles[(self.x, self.y)].x -= 1
                    self.simulation.smoke_particles[(self.x, self.y)].y += 1
                self.y -= 1
                self.x += 1


            if left_below is False: # particle falls to the left
                self.simulation.smoke_map[self.y - 1][self.x - 1], self.simulation.smoke_map[self.y][self.x] = 1, self.simulation.smoke_map[self.y - 1][self.x - 1]  # swap particles on the map
                self.simulation.smoke_particles[(self.x - 1, self.y - 1)], self.simulation.smoke_particles[(self.x, self.y)] = self, self.simulation.smoke_particles[(self.x - 1, self.y - 1)]
                if self.simulation.smoke_particles[(self.x, self.y)] is not None:
                    self.simulation.smoke_particles[(self.x, self.y)].x += 1
                    self.simulation.smoke_particles[(self.x, self.y)].y += 1
                self.y -= 1
                self.x -= 1

        # elif self.y - 1 >= 0 and self.simulation.smoke_map[self.y - 1][self.x] in self.simulation.LIQUIDS:
        #     # if self.y - splash_height - 1 >= 0:
        #     #     increment = 0
        #     #     while self.y - increment >= 0:
        #     #         increment += 1
        #     #         if self.simulation.smoke_map[self.y - increment][self.x] not in self.simulation.LIQUIDS:
        #     #             self.simulation.smoke_map[self.y - 1][self.x], self.simulation.smoke_map[self.y - increment][self.x] = 1, self.simulation.smoke_map[self.y - 1][self.x] # add the sand back 1 square lower
        #     #             self.simulation.smoke_particles[(self.x, self.y - 1)], self.simulation.smoke_particles[(self.x, self.y - increment)] = self, self.simulation.smoke_particles[(self.x, self.y - 1)]
        #     #             self.simulation.smoke_particles[(self.x, self.y - increment)].y -= increment - 1
        #     #             self.y -= 1
        #     #             break
        #     # if self.y - splash_height - 1 >= 0:
        #     #     increment = 0
        #     #     while self.y - increment >= 0:
        #     #         increment += 1
        #     #         if self.simulation.smoke_map[self.y - increment][self.x] == 0:
        #     #             self.simulation.smoke_map[self.y][self.x] = 0
        #     #             self.simulation.smoke_particles[(self.x, self.y)] = None
        #     #             self.simulation.smoke_map[self.y - 1][self.x], self.simulation.smoke_map[self.y - increment][self.x] = 1, self.simulation.smoke_map[self.y - 1][self.x]
        #     #             self.simulation.smoke_particles[(self.x, self.y - 1)], self.simulation.smoke_particles[(self.x, self.y - increment)] = self, self.simulation.smoke_particles[(self.x, self.y - 1)]
        #     #             self.simulation.smoke_particles[(self.x, self.y - increment)].y -= increment + 1
        #     #             self.y -= 1
        #     #             break
        #     self.simulation.smoke_map[self.y - 1][self.x], self.simulation.smoke_map[self.y][self.x] = 1, self.simulation.smoke_map[self.y - 1][self.x]
        #     self.simulation.smoke_particles[(self.x, self.y - 1)], self.simulation.smoke_particles[(self.x, self.y)] = self, self.simulation.smoke_particles[(self.x, self.y - 1)]
        #     self.simulation.smoke_particles[(self.x, self.y)].y += 1
        #     self.y -= 1
        elif self.y - 1 >= 0 and self.simulation.smoke_map[self.y - 1][self.x] == 0: # check if there is a solid object or border under the sand
            self.simulation.smoke_map[self.y][self.x] = 0 # reset the current square
            self.simulation.smoke_map[self.y - 1][self.x] = 1 # add the sand back 1 square lower
            self.simulation.smoke_particles[(self.x, self.y)] = None
            self.simulation.smoke_particles[(self.x, self.y - 1)] = self
            self.y -= 1