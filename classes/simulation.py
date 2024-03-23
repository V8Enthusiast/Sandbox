import pygame
from physics import sand
from physics import water

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
        self.SOLIDS = [STONE, WOOD]
        self.MOVING_SOLIDS = [SAND]
        self.LIQUIDS = [WATER]
        self.window = self.app.screen
        self.buttons = []
        self.particle_size = 10 # the length of all particles (in pixels, 1 for perfect detail)
        self.COLUMNS = self.app.width // self.particle_size
        self.ROWS = self.app.height // self.particle_size
        self.map = [[AIR for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
        self.particles = {}
        for y in range(self.ROWS):
            for x in range(self.COLUMNS):
                self.particles[(x, y)] = None
        print(self.particles)
        self.selected_material = SAND
        self.add_material_on = False

    def render(self):
        self.window.fill((33, 33, 33))
        if self.add_material_on:
            self.add_material()
        for y in range(1, self.ROWS + 1):
            for x in range(1, self.COLUMNS + 1):
                if self.particles[(self.COLUMNS - x, self.ROWS - y)] is not None:
                    self.particles[(self.COLUMNS - x, self.ROWS - y)].render()
        for value in self.particles.values():
            if value is not None:
                value.rendered = False

    # Overrides the default events function in app.py
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_material = SAND
                if event.key == pygame.K_2:
                    self.selected_material = WATER
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
            self.particles[(clicked_column, clicked_row + 1)] = sand.SandParticle(self, clicked_column, clicked_row + 1, (230, 200, 0), 0)
            self.particles[(clicked_column, clicked_row - 1)] = sand.SandParticle(self, clicked_column, clicked_row - 1, (230, 200, 0), 0)
            self.particles[(clicked_column - 1, clicked_row)] = sand.SandParticle(self, clicked_column - 1, clicked_row, (230, 200, 0), 0)
            self.particles[(clicked_column + 1, clicked_row)] = sand.SandParticle(self, clicked_column + 1, clicked_row, (230, 200, 0), 0)
            self.particles[(clicked_column - 1, clicked_row - 1)] = sand.SandParticle(self, clicked_column - 1, clicked_row - 1, (230, 200, 0), 0)
            self.particles[(clicked_column + 1, clicked_row + 1)] = sand.SandParticle(self, clicked_column + 1, clicked_row + 1, (230, 200, 0), 0)
            self.particles[(clicked_column + 1, clicked_row - 1)] = sand.SandParticle(self, clicked_column + 1, clicked_row - 1, (230, 200, 0), 0)
            self.particles[(clicked_column - 1, clicked_row + 1)] = sand.SandParticle(self, clicked_column - 1, clicked_row + 1, (230, 200, 0), 0)
        if self.selected_material == WATER:
            self.particles[(clicked_column, clicked_row)] = water.WaterParticle(self, clicked_column, clicked_row, (90, 188, 216))
            self.particles[(clicked_column, clicked_row + 1)] = water.WaterParticle(self, clicked_column, clicked_row + 1,(90, 188, 216))
            self.particles[(clicked_column, clicked_row - 1)] = water.WaterParticle(self, clicked_column, clicked_row - 1,(90, 188, 216))
            self.particles[(clicked_column - 1, clicked_row)] = water.WaterParticle(self, clicked_column - 1, clicked_row,(90, 188, 216))
            self.particles[(clicked_column + 1, clicked_row)] = water.WaterParticle(self, clicked_column + 1, clicked_row,(90, 188, 216))
            self.particles[(clicked_column - 1, clicked_row - 1)] = water.WaterParticle(self, clicked_column - 1, clicked_row - 1,(90, 188, 216))
            self.particles[(clicked_column + 1, clicked_row + 1)] = water.WaterParticle(self, clicked_column + 1, clicked_row + 1,(90, 188, 216))
            self.particles[(clicked_column + 1, clicked_row - 1)] = water.WaterParticle(self, clicked_column + 1, clicked_row - 1,(90, 188, 216))
            self.particles[(clicked_column - 1, clicked_row + 1)] = water.WaterParticle(self, clicked_column - 1, clicked_row + 1,(90, 188, 216))
        self.map[clicked_row][clicked_column] = self.selected_material
        self.map[clicked_row + 1][clicked_column] = self.selected_material
        self.map[clicked_row - 1][clicked_column] = self.selected_material
        self.map[clicked_row][clicked_column + 1] = self.selected_material
        self.map[clicked_row][clicked_column - 1] = self.selected_material
        self.map[clicked_row - 1][clicked_column - 1] = self.selected_material
        self.map[clicked_row + 1][clicked_column - 1] = self.selected_material
        self.map[clicked_row + 1][clicked_column + 1] = self.selected_material
        self.map[clicked_row - 1][clicked_column + 1] = self.selected_material
