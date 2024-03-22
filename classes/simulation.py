import pygame
from physics import sand

# references used for clearer code
AIR = 0
SAND = 1
WATER = 2
STONE = 3
ACID = 4
FIRE = 5
WOOD = 6

class Simulation:
    def __init__(self, app):
        self.app = app
        self.gravity = 9.81
        self.SOLIDS = [SAND, STONE, WOOD]
        self.window = self.app.screen
        self.buttons = []
        self.particle_size = 5 # the length of all particles (in pixels, 1 for perfect detail)
        self.map = [[AIR for _ in range(self.app.width//self.particle_size)] for i in range(self.app.height//self.particle_size)]
        self.particles = {}
        for y in range(self.app.height//self.particle_size):
            for x in range(self.app.width//self.particle_size):
                self.particles[(x, y)] = None
        print(self.particles)
        self.selected_material = SAND
        self.COLUMNS = self.app.width//self.particle_size
        self.ROWS = self.app.height//self.particle_size
        self.add_material_on = False

    def render(self):
        self.window.fill((33, 33, 33))
        if self.add_material_on:
            self.add_material()
        for row_idx, row in enumerate(self.map):
            for particle_idx, particle in enumerate(row):
                if self.particles[(particle_idx, row_idx)] is not None:
                    self.particles[(particle_idx, row_idx)].render()
        for value in self.particles.values():
            if value is not None:
                value.rendered = False

    # Overrides the default events function in app.py
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.add_material_on = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.add_material_on = False

    def add_material(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked_row = int(mouse_y) // self.particle_size
        clicked_column = int(mouse_x) // self.particle_size
        if clicked_column >= self.COLUMNS or clicked_row >= self.ROWS:
            return
        if self.map[clicked_row][clicked_column] == self.selected_material:
            return
        if self.selected_material == SAND:
            self.particles[(clicked_column, clicked_row)] = sand.SandParticle(self, clicked_column, clicked_row, (230, 200, 0), 0)
        self.map[clicked_row][clicked_column] = self.selected_material
        #print(self.map)
        # doesnt add material when column >=180
