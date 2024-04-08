import random
from classes import simulation

import pygame

class HotbarButton:
    def __init__(self, width, height, x, y, translucent, font, image, bgcolor, fgcolor, function, app, simulation):
        # Save the data passed into the function to variables
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font_type = font
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.app = app
        self.simulation = simulation
        if image != 'sand' and image != 'water':
            self.image = pygame.image.load(f"img/sand.png").convert()
        else:
            self.image = pygame.image.load(f"img/{image}.png").convert()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.border = 2
        self.function = function

        pygame.font.init()

    def render(self):
        # Put together the button based on the parameters
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.simulation.selected_button == self.function:
            #self.bgcolor = (200, 200, 200)
            self.bgcolor = self.simulation.hotbar_color
        else:
            self.bgcolor = (0, 0, 0)

        # Draw the button
        pygame.draw.rect(self.app.screen, self.bgcolor, self.rect)
        self.app.screen.blit(self.image, (self.x - self.border, self.y - self.border))

    def click(self):
        if self.function == 'sand':
            self.simulation.selected_material = 1
        elif self.function == 'water':
            self.simulation.selected_material = 2
        elif self.function == 'stone':
            self.simulation.selected_material = 3
        elif self.function == 'acid':
            self.simulation.selected_material = 4
        elif self.function == 'plastic':
            self.simulation.selected_material = 5
        elif self.function == 'fire':
            self.simulation.selected_material = 6
        elif self.function == 'oil':
            self.simulation.selected_material = 8
        elif self.function == 'iron':
            self.simulation.selected_material = 10
        elif self.function == 'gold':
            self.simulation.selected_material = 11
        elif self.function == 'copper':
            self.simulation.selected_material = 12
        elif self.function == 'eraser':
            self.simulation.selected_material = 0
        else:
            print("unassigned button")