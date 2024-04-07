import pygame
import random

fire_detail = 1
colors = [(222, 64, 24), (222, 126, 24)]

class FireParticle:
    def __init__(self, simulation, x, y, color):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = color
        self.rendered = False
        self.isFalling = False
        self.part_size = self.simulation.particle_size // fire_detail
    def render(self):
        if self.rendered is False:
            for r in range(fire_detail):
                for c in range(fire_detail):
                    if random.randint(0, 100) > 50:
                        rect = pygame.Rect(0, 0, self.part_size, self.part_size)
                        rect.center = (self.x * self.simulation.particle_size - self.simulation.particle_size // 2 + c * self.part_size + self.part_size / 2, self.y * self.simulation.particle_size - self.simulation.particle_size // 2 + r * self.part_size + self.part_size / 2)
                        pygame.draw.rect(self.simulation.window, random.choice(colors), rect)
            self.calculate_physics()
            self.rendered = True
            print("dsdsd")

    def calculate_physics(self):
        self.simulation.heat_map[self.y - 1][self.x] += 5