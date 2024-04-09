import pygame
import random
import functions
from physics import fire, ash, smoke

fire_detail = 1
colors = [(222, 64, 24), (222, 126, 24)]

class OilParticle:
    def __init__(self, simulation, x, y, color):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = color
        self.start_color = color
        self.rendered = False
        self.isFalling = True
        self.strength = 0 # this is needed to calculate dissolving acid
        self.start_fuel = 800
        self.fuel_left = 800 # this variable determines how long the particle will burn if set on fire
        self.flammability = 400 # (0, 1000) this variable determines how easily the particle will catch on fire
        self.chance_to_leave_ash = 0 # (0, 100) variable determines how often the particle leaves ash when finished burning (0 for no ash)
        self.isOnFire = False
        self.part_size = self.simulation.particle_size // fire_detail

    def render(self):
        if self.rendered is False:
            if self.isOnFire:
                for r in range(fire_detail):
                    for c in range(fire_detail):
                        rect = pygame.Rect(0, 0, self.part_size, self.part_size)
                        rect.center = (
                        self.x * self.simulation.particle_size - self.simulation.particle_size // 2 + c * self.part_size + self.part_size / 2,
                        self.y * self.simulation.particle_size - self.simulation.particle_size // 2 + r * self.part_size + self.part_size / 2)
                        if random.randint(0, 100) > 50:
                            pygame.draw.rect(self.simulation.window, random.choice(colors), rect)
                        else:
                            pygame.draw.rect(self.simulation.window, self.color, rect)
            else:
                rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
                rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
                pygame.draw.rect(self.simulation.window, self.color, rect)
            self.calculate_physics()
            self.rendered = True

    def swap_particle_with_fire(self, x, y):
        if random.randint(0, 1000) < self.simulation.particles[(x, y)].flammability:
            if self.simulation.map[y][x] != 8 and self.simulation.map[y][x] != 13: # oil
                fuel = self.simulation.particles[(x, y)].fuel
                color = self.simulation.particles[(x, y)].color
                burning_material = self.simulation.map[y][x]
                chance_to_leave_ash = self.simulation.particles[(x, y)].chance_to_leave_ash_particle
                self.simulation.map[y][x] = 6
                self.simulation.particles[(x, y)] = fire.FireParticle(self.simulation, x, y, color)
                self.simulation.particles[(x, y)].fuel_left = fuel
                self.simulation.particles[(x, y)].start_fuel = fuel
                self.simulation.particles[(x, y)].burning_material = burning_material
                if chance_to_leave_ash > 0:
                    self.simulation.particles[(x, y)].chance_to_leave_ash = chance_to_leave_ash
            else:
                self.simulation.particles[(x, y)].isOnFire = True
    def spread_fire(self):
        # above particle
        if self.y - 1 >= 0:
            if self.simulation.map[self.y - 1][self.x] in self.simulation.FLAMMABLE_PARTICLES:
                self.swap_particle_with_fire(self.x, self.y - 1)
            if self.x - 1 >= 0 and self.simulation.map[self.y - 1][self.x - 1] in self.simulation.FLAMMABLE_PARTICLES:
                self.swap_particle_with_fire(self.x - 1, self.y - 1)
            if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y - 1][self.x + 1] in self.simulation.FLAMMABLE_PARTICLES:
                self.swap_particle_with_fire(self.x + 1, self.y - 1)
        # on the same level as particle
        if self.x - 1 >= 0 and self.simulation.map[self.y][self.x - 1] in self.simulation.FLAMMABLE_PARTICLES:
            self.swap_particle_with_fire(self.x - 1, self.y)
        if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y][self.x + 1] in self.simulation.FLAMMABLE_PARTICLES:
            self.swap_particle_with_fire(self.x + 1, self.y)
        # below particle
        if self.y + 1 < self.simulation.ROWS:
            if self.simulation.map[self.y + 1][self.x] in self.simulation.FLAMMABLE_PARTICLES:
                self.swap_particle_with_fire(self.x, self.y + 1)
            if self.x - 1 >= 0 and self.simulation.map[self.y + 1][self.x - 1] in self.simulation.FLAMMABLE_PARTICLES:
                self.swap_particle_with_fire(self.x - 1, self.y + 1)
            if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y + 1][self.x + 1] in self.simulation.FLAMMABLE_PARTICLES:
                self.swap_particle_with_fire(self.x + 1, self.y + 1)

    def calculate_physics(self):
        if self.isOnFire:
            self.spread_fire()
            if self.fuel_left > 0:
                self.simulation.heat_map[self.y - 1][self.x] += 10
                self.fuel_left -= 1
                self.color = functions.mix_colors(self.start_color, (10, 10, 10),
                                                                   self.fuel_left / self.start_fuel)
            else:
                if self.chance_to_leave_ash > 0 and random.randint(0, 100) < self.chance_to_leave_ash:
                    self.simulation.map[self.y][self.x] = 9
                    self.simulation.particles[(self.x, self.y)] = ash.AshParticle(self.simulation, self.x, self.y)
                else:
                    self.simulation.map[self.y][self.x] = 0
                    self.simulation.particles[(self.x, self.y)] = None
                    self.simulation.smoke_particles[(self.x, self.y)] = smoke.SmokeParticle(self.simulation, self.x, self.y, 'CO2')
                    self.simulation.smoke_map[self.y][self.x] = 1

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
                    self.simulation.map[self.y + 1][first_empty_particle_left_x] = 8  # add the water to the chosen square
                    self.simulation.particles[(self.x, self.y)] = None
                    self.simulation.particles[(first_empty_particle_left_x, self.y + 1)] = self
                    self.y += 1
                    self.x = first_empty_particle_left_x

                if first_empty_particle_right_x is not None:
                    self.simulation.map[self.y][self.x] = 0  # reset the current square
                    self.simulation.map[self.y + 1][first_empty_particle_right_x] = 8  # add the water to the chosen square
                    self.simulation.particles[(self.x, self.y)] = None
                    self.simulation.particles[(first_empty_particle_right_x, self.y + 1)] = self
                    self.y += 1
                    self.x = first_empty_particle_right_x

            elif self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] not in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS + self.simulation.LIQUIDS: # water is on top of air
                self.simulation.map[self.y][self.x] = 0 # reset the current square
                self.simulation.map[self.y + 1][self.x] = 8 # add the sand back 1 square lower
                self.simulation.particles[(self.x, self.y)] = None
                self.simulation.particles[(self.x, self.y + 1)] = self
                self.y += 1