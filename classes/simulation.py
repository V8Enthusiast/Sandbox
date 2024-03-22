import pygame

class Simulation:
    def __init__(self, app):
        self.app = app
        self.window = self.app.screen
        self.buttons = []

    def render(self):
        self.window.fill((33, 33, 33))
        pass
