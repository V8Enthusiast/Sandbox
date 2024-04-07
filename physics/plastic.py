import pygame
import random

class PlasticParticle:
    def __init__(self, simulation, x, y, color):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = color
        self.rendered = False
        self.isFalling = False
        self.fuel = 100 # this variable determines how long the particle will burn if set on fire
        self.flammability = 50 # (0, 1000) this variable determines how easily the particle will catch on fire
        self.chance_to_leave_ash_particle = 30 # (0, 100) variable determines how often the particle leaves ash when finished burning (0 for no ash)
    def render(self):
        if self.rendered is False:
            rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
            rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
            pygame.draw.rect(self.simulation.window, self.color, rect)
            self.rendered = True