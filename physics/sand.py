import pygame

class SandParticle:
    def __init__(self, simulation, x, y, color, wetness):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = color
        self.wetness = wetness

    def render(self):
        rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
        rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
        pygame.draw.rect(self.simulation.window, self.color, rect)
        self.calculate_physics()

    def calculate_physics(self):
        if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] not in self.simulation.SOLIDS: # check if there is a solid object or border under the sand
            self.simulation.map[self.y][self.x] = 0 # reset the current square
            self.simulation.map[self.y + 1][self.x] = 1 # add the sand back 1 square lower
            self.simulation.particles[(self.x, self.y)] = None
            self.simulation.particles[(self.x, self.y + 1)] = self
            self.y += 1



