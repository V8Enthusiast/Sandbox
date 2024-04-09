import pygame
import random

import functions
from physics import plastic, oil, smoke

FIRE = 6
OIL = 8

fully_melted_color = (252, 22, 18)

class MetalParticle:
    def __init__(self, simulation, x, y, color, melting_temp, solidify_temp):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.base_color = color
        self.color = color
        self.temp = self.simulation.base_temp
        self.solidify_temp = solidify_temp
        self.melting_temp = melting_temp
        self.rendered = False
        self.isFalling = False
        self.isLiquid = False
        # self.strength = 0 # this is needed to calculate dissolving acid

    def render(self):
        if self.rendered is False:
            rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
            rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
            pygame.draw.rect(self.simulation.window, self.color, rect)
            if self.simulation.heat_map[self.y][self.x] != self.temp:
                diff = abs(self.simulation.heat_map[self.y][self.x] - self.temp)
                if self.simulation.heat_map[self.y][self.x] > self.temp:
                    self.temp += diff / 2
                elif self.simulation.heat_map[self.y][self.x] < self.temp:
                    self.temp -= diff / 2
            if self.temp >= self.melting_temp or self.isLiquid and self.temp > self.solidify_temp:
                self.isLiquid = True
            else:
                self.isLiquid = False
                self.isFalling = False
            self.color = functions.mix_colors(fully_melted_color, self.base_color, min((max(self.temp - 20, 0))/self.melting_temp, 1))
            self.calculate_physics()
            self.rendered = True

    def put_out_fire(self, x, y):
        if self.simulation.map[y][x] == OIL:
            self.simulation.particles[(x, y)].isOnFire = False
            self.simulation.map[self.y][self.x] = 0  # reset the current square
            self.simulation.particles[(self.x, self.y)] = None
            self.simulation.smoke_map[y][x] = 1
            self.simulation.smoke_particles[(x, y)] = smoke.SmokeParticle(self.simulation, x, y, 'H2')
        elif self.simulation.particles[(x, y)].burning_material is not None:
            self.simulation.map[self.y][self.x] = 0  # reset the current square
            self.simulation.map[y][x] = self.simulation.particles[(x, y)].burning_material
            self.simulation.smoke_map[y][x] = 1
            self.simulation.smoke_particles[(x, y)] = smoke.SmokeParticle(self.simulation, x, y, 'H2')
            self.simulation.particles[(self.x, self.y)] = None
            if self.simulation.particles[(x, y)].burning_material == 5: # Plastic
                self.simulation.particles[(x, y)] = plastic.PlasticParticle(self.simulation, x, y, self.simulation.particles[(x, y)].burning_material_color)
        else:
            self.simulation.map[self.y][self.x] = 0  # reset the current square
            self.simulation.map[y][x] = 0
            self.simulation.smoke_map[y][x] = 1
            self.simulation.smoke_particles[(x, y)] = smoke.SmokeParticle(self.simulation, x, y, 'H2')
            self.simulation.particles[(self.x, self.y)] = None
            self.simulation.particles[(x, y)] = None


    def calculate_physics(self):
        if self.isLiquid:
            # checks if at least one particle under is air
            if self.y + 1 < self.simulation.ROWS and ((self.simulation.map[self.y + 1][self.x] == 0 or self.simulation.particles[(self.x, self.y + 1)].isFalling) or (self.x + 1 < self.simulation.COLUMNS and (self.simulation.map[self.y + 1][self.x + 1] == 0 or self.simulation.particles[(self.x + 1, self.y + 1)].isFalling)) or (self.x - 1 >= 0 and (self.simulation.map[self.y + 1][self.x - 1] == 0 or self.simulation.particles[(self.x - 1, self.y + 1)].isFalling))):
                self.isFalling = True
            # checks if the particle is covered by a liquid
            if self.y - 1 >= 0 and (self.simulation.map[self.y - 1][self.x] not in self.simulation.LIQUIDS or (self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y - 1][self.x + 1] == 0) or (self.x - 1 >= 0 and self.simulation.map[self.y - 1][self.x - 1] == 0)):
                self.isFalling = True

            if self.isFalling:
                if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] != 0 and self.simulation.particles[(self.x, self.y + 1)].isFalling is False:
                    self.isFalling = False
                elif self.y + 1 >= self.simulation.ROWS:
                    self.isFalling = False

                # if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] == 0:
                #     self.isFalling = True

                if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] != 0 and self.isFalling is False: # particle under is not air

                    # to the right
                    first_empty_particle_right_x = None
                    for i in range(1, self.simulation.COLUMNS - self.x):
                        if self.simulation.map[self.y + 1][self.x + i] == 0:
                            first_empty_particle_right_x = self.x + i
                            break
                        elif self.simulation.map[self.y + 1][self.x + i] == FIRE or (self.simulation.map[self.y + 1][self.x + i] == OIL and self.simulation.particles[(self.x + i, self.y + 1)].isOnFire):
                            self.put_out_fire(self.x + i, self.y + 1)
                            break
                        if self.simulation.map[self.y + 1][self.x + i] in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS:
                            break

                    # to the left
                    first_empty_particle_left_x = None
                    for n in range(1, self.x):
                        if self.simulation.map[self.y + 1][self.x - n] == 0:
                            first_empty_particle_left_x = self.x - n
                            break
                        elif self.simulation.map[self.y + 1][self.x - n] == FIRE or (self.simulation.map[self.y + 1][self.x - n] == OIL and self.simulation.particles[(self.x - n, self.y + 1)].isOnFire):
                            self.put_out_fire(self.x - n, self.y + 1)
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
                        self.simulation.map[self.y + 1][first_empty_particle_left_x] = 10  # add the water to the chosen square
                        self.simulation.particles[(self.x, self.y)] = None
                        self.simulation.particles[(first_empty_particle_left_x, self.y + 1)] = self
                        self.y += 1
                        self.x = first_empty_particle_left_x

                    if first_empty_particle_right_x is not None:
                        self.simulation.map[self.y][self.x] = 0  # reset the current square
                        self.simulation.map[self.y + 1][first_empty_particle_right_x] = 10  # add the water to the chosen square
                        self.simulation.particles[(self.x, self.y)] = None
                        self.simulation.particles[(first_empty_particle_right_x, self.y + 1)] = self
                        self.y += 1
                        self.x = first_empty_particle_right_x

                elif self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] not in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS + self.simulation.LIQUIDS: # water is on top of air
                    self.simulation.map[self.y][self.x] = 0 # reset the current square
                    self.simulation.map[self.y + 1][self.x] = 10 # add the sand back 1 square lower
                    self.simulation.particles[(self.x, self.y)] = None
                    self.simulation.particles[(self.x, self.y + 1)] = self
                    self.y += 1
            if self.y + 1 < self.simulation.ROWS and (self.simulation.map[self.y + 1][self.x] == FIRE or (self.simulation.map[self.y + 1][self.x] == OIL and self.simulation.particles[(self.x, self.y + 1)].isOnFire)):  # water is on top of fire
                self.put_out_fire(self.x, self.y + 1)