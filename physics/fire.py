import pygame
import random
import functions
from physics import ash, smoke

fire_detail = 1
colors = [(222, 64, 24), (222, 126, 24)]

class FireParticle:
    def __init__(self, simulation, x, y, burning_material_color):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.burning_material_color = burning_material_color
        self.color = burning_material_color
        self.rendered = False
        self.isFalling = False
        self.part_size = self.simulation.particle_size // fire_detail
        self.burning_material = None
        self.fuel_left = 15
        self.start_fuel = 15
        self.chance_to_leave_ash = 0
    def render(self):
        if self.rendered is False:
            for r in range(fire_detail):
                for c in range(fire_detail):
                    rect = pygame.Rect(0, 0, self.part_size, self.part_size)
                    rect.center = (self.x * self.simulation.particle_size - self.simulation.particle_size // 2 + c * self.part_size + self.part_size / 2, self.y * self.simulation.particle_size - self.simulation.particle_size // 2 + r * self.part_size + self.part_size / 2)
                    if random.randint(0, 100) > 50:
                        pygame.draw.rect(self.simulation.window, random.choice(colors), rect)
                    else:
                        pygame.draw.rect(self.simulation.window, self.color, rect)

            self.calculate_physics()
            self.rendered = True

    def swap_particle_with_fire(self, x, y):
        if random.randint(0, 1000) < self.simulation.particles[(x, y)].flammability:
            if self.simulation.map[y][x] != 8 and self.simulation.map[y][x] != 13:  # oil # hydrogen
                fuel = self.simulation.particles[(x, y)].fuel
                color = self.simulation.particles[(x, y)].color
                burning_material = self.simulation.map[y][x]
                chance_to_leave_ash = self.simulation.particles[(x, y)].chance_to_leave_ash_particle
                self.simulation.map[y][x] = 6
                self.simulation.particles[(x, y)] = FireParticle(self.simulation, x, y, color)
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

        self.spread_fire()
        if self.fuel_left > 0:
            self.simulation.heat_map[self.y - 1][self.x] += 10
            self.fuel_left -= 1
            if self.burning_material_color != self.simulation.bg_color:
                self.color = functions.mix_colors(self.burning_material_color,(10, 10, 10), self.fuel_left / self.start_fuel)
        else:
            if self.chance_to_leave_ash > 0 and random.randint(0, 100) < self.chance_to_leave_ash:
                self.simulation.map[self.y][self.x] = 9
                self.simulation.particles[(self.x, self.y)] = ash.AshParticle(self.simulation, self.x, self.y)
            else:
                self.simulation.map[self.y][self.x] = 0
                self.simulation.particles[(self.x, self.y)] = None
                self.simulation.smoke_particles[(self.x, self.y)] = smoke.SmokeParticle(self.simulation, self.x, self.y,'CO2')
                self.simulation.smoke_map[self.y][self.x] = 1

