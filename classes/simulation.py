import random

import pygame
from physics import sand, water, stone, acid, plastic, fire
import functions

# references used for clearer code
AIR = 0
SAND = 1
WATER = 2
STONE = 3
ACID = 4
PLASTIC = 5
FIRE = 6
WOOD = 7

class Simulation:
    def __init__(self, app):
        self.app = app
        self.gravity = 9.81
        self.base_temp = 20
        self.SOLIDS = [STONE, WOOD, PLASTIC]
        self.MOVING_SOLIDS = [SAND]
        self.LIQUIDS = [WATER, ACID]
        self.NON_ACIDIC_LIQUIDS = [WATER]
        self.NON_DISSOLVABLE_PARTICLES = [ACID, PLASTIC]
        self.window = self.app.screen
        self.buttons = []
        self.particle_size = 5 # the length of all particles (in pixels, 1 for perfect detail)
        self.COLUMNS = self.app.width // self.particle_size
        self.ROWS = self.app.height // self.particle_size
        self.map = [[AIR for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
        self.heat_map = [[20 for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
        self.particles = {}
        self.place_radius = 1
        for y in range(self.ROWS):
            for x in range(self.COLUMNS):
                self.particles[(x, y)] = None
        self.selected_material = SAND
        self.add_material_on = False
        self.active_water_particles = 0

    def render(self):
        self.window.fill((33, 33, 33))
        if self.add_material_on:
            self.add_material()
        for y in range(1, self.ROWS + 1):
            for x in range(1, self.COLUMNS + 1):
                r = self.ROWS - y
                c = self.COLUMNS - x
                if self.particles[(c, r)] is not None:
                    self.particles[(c, r)].render()
                else:
                    if r + 1 < self.ROWS and self.heat_map[r + 1][c] > self.heat_map[r][c]:
                        diff = self.heat_map[r + 1][c] - self.heat_map[r][c]
                        self.heat_map[r + 1][c] -= diff
                        self.heat_map[r][c] += diff
                    if self.heat_map[r][c] != self.base_temp:
                        # heat visualization
                        scale = self.heat_map[r][c]/100
                        if scale > 1:
                            scale = 1
                        color = functions.mix_colors((255, 0, 0), (15, 15, 15), scale)
                        rect = pygame.Rect(0, 0, self.particle_size, self.particle_size)
                        rect.center = ((c) * self.particle_size, (r) * self.particle_size)
                        pygame.draw.rect(self.window, color, rect)

        for value in self.particles.values():
            if value is not None:
                value.rendered = False
        #print(self.active_water_particles)
        self.active_water_particles = 0
        self.render_hotbar()

    def render_hotbar(self):
        hotbar_rect = pygame.Rect(0, self.app.height - 2, self.app.width, self.app.hotbar_height)
        pygame.draw.rect(self.window, (150, 150, 150) ,hotbar_rect)

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
                if event.key == pygame.K_3:
                    self.selected_material = STONE
                if event.key == pygame.K_4:
                    self.selected_material = ACID
                if event.key == pygame.K_5:
                    self.selected_material = PLASTIC
                if event.key == pygame.K_6:
                    self.selected_material = FIRE
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
            #self.particles[(clicked_column, clicked_row)] = sand.SandParticle(self, clicked_column, clicked_row, (230, 200, 0), 0)
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    if random.randint(0, 100) > 65:
                        try:
                            self.map[y][x] = self.selected_material
                            self.particles[(x, y)] = sand.SandParticle(self, x, y, (230, 200, 0), 0)
                        except:
                            pass

        if self.selected_material == WATER:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    if random.randint(0, 100) > 10:
                        try:
                            self.map[y][x] = self.selected_material
                            self.particles[(x, y)] = water.WaterParticle(self, x, y, (90, 188, 216))
                        except:
                            pass

        if self.selected_material == STONE:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    self.map[y][x] = self.selected_material
                    self.particles[(x, y)] = stone.StoneParticle(self, x, y, (136, 140, 141))

        if self.selected_material == ACID:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    if random.randint(0, 100) > 75:
                        try:
                            self.map[y][x] = self.selected_material
                            self.particles[(x, y)] = acid.AcidParticle(self, x, y, (102, 242, 15))
                        except:
                            pass

        if self.selected_material == PLASTIC:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    self.map[y][x] = self.selected_material
                    self.particles[(x, y)] = plastic.PlasticParticle(self, x, y, (215, 215, 215))

        if self.selected_material == FIRE:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    self.map[y][x] = self.selected_material
                    self.particles[(x, y)] = fire.FireParticle(self, x, y, (222, 64, 24))