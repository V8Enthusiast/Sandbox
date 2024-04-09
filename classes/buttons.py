import random
from classes import simulation

import pygame

class Button:
    def __init__(self, width, height, x, y, translucent, font, text, bgcolor, fgcolor, function, app):
        # Save the data passed into the function to variables
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font_type = font
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.app = app
        self.text = text
        self.function = function

        pygame.font.init()

    def render(self):
        # Put together the button based on the parameters
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font(self.font_type, int(32 * self.app.scale))
        self.display_text = self.font.render(self.text, True, self.fgcolor)
        # Get the textbox rect and align its center with the center of the button rect
        self.display_text_rect = self.display_text.get_rect()
        self.display_text_rect.center = self.rect.center
        # Draw the button
        pygame.draw.rect(self.app.screen, self.bgcolor, self.rect)
        self.app.screen.blit(self.display_text, self.display_text_rect)
    def click(self):
        if self.function == 'play':
            self.app.ui = simulation.Simulation(self.app) # Change the displayed ui to a new simulation
        if self.function == 'back':
            self.app.ui = self.app.active_simulation # Change the displayed ui back to the simulation
            self.app.active_simulation = None
        else:
            self.bgcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))