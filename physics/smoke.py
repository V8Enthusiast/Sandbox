import pygame
import random
import functions
from physics import ash, fire

h2o = [(158, 158, 158), (169, 169, 169), (77, 77, 77)]
h2 = [(228, 228, 228), (200, 200, 200), (177, 177, 177)]
co2 = [(58, 58, 58), (69, 69, 69), (97, 97, 97)]
colors = [h2o, h2, co2]
types = {'H2O':0, 'H2':1, 'CO2':2}

fire_detail = 1
fire_colors = [(222, 64, 24), (222, 126, 24)]

class SmokeParticle:
    def __init__(self, simulation, x, y, type):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = random.choice(colors[types[type]])
        self.rendered = False
        self.type = type
        self.isFalling = True
        self.isOnFire = False
        if self.type == 'H2':
            self.start_color = self.color
            self.start_fuel = 400
            self.fuel_left = 400  # this variable determines how long the particle will burn if set on fire
            self.flammability = 900  # (0, 1000) this variable determines how easily the particle will catch on fire
            self.chance_to_leave_ash = 10  # (0, 100) variable determines how often the particle leaves ash when finished burning (0 for no ash)
            self.map = self.simulation.map
            self.particles = self.simulation.particles
            self.part_size = self.simulation.particle_size // fire_detail
            self.id = 13 # Hydrogen
        else:
            self.id = 1
            self.map = self.simulation.smoke_map
            self.particles = self.simulation.smoke_particles
    def render(self):
        if self.rendered is False:
            if self.type == 'H2' and self.map == self.simulation.smoke_map:
                if self.simulation.map[self.y][self.x] == 0:
                    self.simulation.map[self.y][self.x] = self.id
                    self.simulation.particles[(self.x, self.y)] = self
                    self.simulation.smoke_map[self.y][self.x] = 0
                    self.simulation.smoke_particles[(self.x, self.y)] = None
                    self.map = self.simulation.map
                    self.particles = self.simulation.particles

            if self.isOnFire:
                for r in range(fire_detail):
                    for c in range(fire_detail):
                        rect = pygame.Rect(0, 0, self.part_size, self.part_size)
                        rect.center = (
                            self.x * self.simulation.particle_size - self.simulation.particle_size // 2 + c * self.part_size + self.part_size / 2,
                            self.y * self.simulation.particle_size - self.simulation.particle_size // 2 + r * self.part_size + self.part_size / 2)
                        if random.randint(0, 100) > 50:
                            pygame.draw.rect(self.simulation.window, random.choice(fire_colors), rect)
                        else:
                            pygame.draw.rect(self.simulation.window, self.color, rect)
            else:
                rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
                rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
                pygame.draw.rect(self.simulation.window, self.color, rect)
            self.calculate_physics()
            self.rendered = True
            #self.color = random.choice(colors)

    def swap_particle_with_fire(self, x, y):
        if random.randint(0, 1000) < self.simulation.particles[(x, y)].flammability:
            if self.simulation.map[y][x] != 8 and self.simulation.map[y][x] != 13:  # oil # hydrogen
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
                if self.start_color != self.simulation.bg_color:
                    self.color = functions.mix_colors(self.start_color, (10, 10, 10),
                                                      self.fuel_left / self.start_fuel)
            else:
                if self.chance_to_leave_ash > 0 and random.randint(0, 100) < self.chance_to_leave_ash:
                    self.simulation.map[self.y][self.x] = 9
                    self.simulation.particles[(self.x, self.y)] = ash.AshParticle(self.simulation, self.x, self.y)
                else:
                    self.simulation.map[self.y][self.x] = 0
                    self.simulation.particles[(self.x, self.y)] = None
                    self.simulation.smoke_particles[(self.x, self.y)] = SmokeParticle(self.simulation, self.x, self.y, 'CO2')
                    self.simulation.smoke_map[self.y][self.x] = 1

        if self.y - 1 >= 0 and self.map[self.y - 1][self.x] != 0 and self.particles[(self.x, self.y - 1)].isFalling is False:
            self.isFalling = False
        elif self.y - 1 < 0:
            self.isFalling = False

        if self.y - 1 >= 0 and self.map[self.y - 1][self.x] == 0:
            self.isFalling = True

        if self.y - 1 >= 0 and self.map[self.y - 1][self.x] != 0 and self.isFalling is False: # particle under is a moving one (sand)
            if self.x + 1 < self.simulation.COLUMNS:
                    right_below = self.map[self.y - 1][self.x + 1] != 0  # checks if the particle should move down to the right
            else:
                right_below = True
            if self.x - 1 >= 0:
                    left_below = self.map[self.y - 1][self.x - 1] != 0 # checks if the particle should move down to the left
            else:
                left_below = True


            if right_below is False and left_below is False: # if both are true choose one side which the particle will head to
                if random.randint(0, 100) >= 50:
                    left_below = True
                else:
                    right_below = True

            if right_below is False: # particle falls to the right
                self.map[self.y - 1][self.x + 1], self.map[self.y][self.x] = self.id, self.map[self.y - 1][self.x + 1] # swap particles on the map
                self.particles[(self.x + 1, self.y - 1)], self.particles[(self.x, self.y)] = self, self.particles[(self.x + 1, self.y - 1)]
                if self.particles[(self.x, self.y)] is not None:
                    self.particles[(self.x, self.y)].x -= 1
                    self.particles[(self.x, self.y)].y += 1
                self.y -= 1
                self.x += 1


            if left_below is False: # particle falls to the left
                self.map[self.y - 1][self.x - 1], self.map[self.y][self.x] = self.id, self.map[self.y - 1][self.x - 1]  # swap particles on the map
                self.particles[(self.x - 1, self.y - 1)], self.particles[(self.x, self.y)] = self, self.particles[(self.x - 1, self.y - 1)]
                if self.particles[(self.x, self.y)] is not None:
                    self.particles[(self.x, self.y)].x += 1
                    self.particles[(self.x, self.y)].y += 1
                self.y -= 1
                self.x -= 1

        # elif self.y - 1 >= 0 and self.map[self.y - 1][self.x] in self.simulation.LIQUIDS:
        #     # if self.y - splash_height - 1 >= 0:
        #     #     increment = 0
        #     #     while self.y - increment >= 0:
        #     #         increment += 1
        #     #         if self.map[self.y - increment][self.x] not in self.simulation.LIQUIDS:
        #     #             self.map[self.y - 1][self.x], self.map[self.y - increment][self.x] = 1, self.map[self.y - 1][self.x] # add the sand back 1 square lower
        #     #             self.particles[(self.x, self.y - 1)], self.particles[(self.x, self.y - increment)] = self, self.particles[(self.x, self.y - 1)]
        #     #             self.particles[(self.x, self.y - increment)].y -= increment - 1
        #     #             self.y -= 1
        #     #             break
        #     # if self.y - splash_height - 1 >= 0:
        #     #     increment = 0
        #     #     while self.y - increment >= 0:
        #     #         increment += 1
        #     #         if self.map[self.y - increment][self.x] == 0:
        #     #             self.map[self.y][self.x] = 0
        #     #             self.particles[(self.x, self.y)] = None
        #     #             self.map[self.y - 1][self.x], self.map[self.y - increment][self.x] = 1, self.map[self.y - 1][self.x]
        #     #             self.particles[(self.x, self.y - 1)], self.particles[(self.x, self.y - increment)] = self, self.particles[(self.x, self.y - 1)]
        #     #             self.particles[(self.x, self.y - increment)].y -= increment + 1
        #     #             self.y -= 1
        #     #             break
        #     self.map[self.y - 1][self.x], self.map[self.y][self.x] = 1, self.map[self.y - 1][self.x]
        #     self.particles[(self.x, self.y - 1)], self.particles[(self.x, self.y)] = self, self.particles[(self.x, self.y - 1)]
        #     self.particles[(self.x, self.y)].y += 1
        #     self.y -= 1
        elif self.y - 1 >= 0 and self.map[self.y - 1][self.x] == 0: # check if there is a solid object or border under the sand
            self.map[self.y][self.x] = 0 # reset the current square
            self.map[self.y - 1][self.x] = self.id # add the sand back 1 square lower
            self.particles[(self.x, self.y)] = None
            self.particles[(self.x, self.y - 1)] = self
            self.y -= 1