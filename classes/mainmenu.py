import random

import pygame
from physics import sand, water, stone, acid, plastic, fire, oil, metal, smoke, chlorine
from classes import buttons
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
OIL = 8
ASH = 9
IRON = 10
GOLD = 11
COPPER = 12
HYDROGEN = 13
CHLORINE = 14

class MainMenu:
    def __init__(self, app):
        self.app = app

        self.main_text_rect_center = (self.app.width // 2, 250 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        self.buttons = [
            buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width / 2 - 100 * self.app.scale,
                           self.app.height / 2 - 75 * self.app.scale / 2, False, self.font, "Play", (0, 0, 0),
                           self.font_color, 'play', self.app)]

        self.materials = [SAND, WATER, STONE, ACID, PLASTIC, FIRE, OIL, IRON, GOLD, COPPER, HYDROGEN, CHLORINE]

        self.gravity = 9.81
        self.bg_color = (33, 33, 33)
        self.base_temp = 20
        self.heat_width = 90 # the higher this value is, the narrower the heat will be
        self.calculate_heat = False
        self.view_heat = False
        self.SOLIDS = [STONE, WOOD, PLASTIC, IRON, GOLD, COPPER]
        self.METALS = [IRON, GOLD, COPPER]
        self.MOVING_SOLIDS = [SAND, ASH, CHLORINE]
        self.LIQUIDS = [WATER, ACID]
        self.NON_ACIDIC_LIQUIDS = [WATER]
        self.NON_DISSOLVABLE_PARTICLES = [ACID, PLASTIC, CHLORINE]
        self.FLAMMABLE_PARTICLES = [PLASTIC, WOOD, OIL, HYDROGEN]
        self.window = self.app.screen
        self.particle_size = 5 # the length of all particles (in pixels, 1 for perfect detail)
        self.COLUMNS = self.app.width // self.particle_size
        self.ROWS = (self.app.height + self.app.hotbar_height) // self.particle_size

        self.max_particles = 650 # self.COLUMNS * self.ROWS // 13
        self.max_metal_particles = (self.max_particles // 12) * 2
        self.max_liquid_particles = (self.max_particles // 12) * 4

        self.active_particles = 0
        self.active_metal_particles = 0
        self.active_liquid_particles = 0


        self.map = [[AIR for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
        self.heat_map = [[20 for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
        self.smoke_map = [[0 for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
        self.particles = {}
        self.smoke_particles = {}
        self.place_radius = 1
        for y in range(self.ROWS):
            for x in range(self.COLUMNS):
                self.particles[(x, y)] = None
                self.smoke_particles[(x, y)] = None
        self.selected_material = SAND
        self.add_material_on = False
        self.active_water_particles = 0
        # self.hotbar_color = (150, 150, 150)
        #
        # # self.side_margin = int(20 * self.app.scale)
        # #
        # # self.button_names = ['sand', 'water', 'stone', 'acid', 'plastic', 'fire', 'oil', 'iron', 'gold', 'copper', 'hydrogen', 'chlorine', 'eraser', 'settings', 'exit']
        # # button_amount = len(self.button_names)
        # # #button_size = (self.app.width - 2 * self.side_margin) // button_amount
        # # button_size = int(64 * self.app.scale)
        # # space_between_buttons = (self.app.width - self.side_margin * 2 - button_amount * button_size) // (button_amount - 1)
        # # height = (self.app.hotbar_height - button_size) // 2
        # # self.hotbar_buttons = []
        # # for idx, button_name in enumerate(self.button_names):
        # #     self.hotbar_buttons.append(hotbar_button.HotbarButton(button_size, button_size, self.side_margin + idx * (button_size + space_between_buttons), self.app.height + height, False, "fonts/main_font.ttf", button_name, (0, 0, 0), (255, 255, 255), button_name, self.app, self))
        # #
        # # self.selected_button = None

    def draw_heat(self, r, c):
        # heat visualization
        scale = self.heat_map[r][c] / 400
        if scale > 1:
            scale = 1
        color = functions.mix_colors((255, 0, 0), self.bg_color, scale)
        rect = pygame.Rect(0, 0, self.particle_size, self.particle_size)
        rect.center = (c * self.particle_size, r * self.particle_size)
        pygame.draw.rect(self.window, color, rect)

    def render(self):
        self.window.fill(self.bg_color)
        if self.add_material_on:
            self.add_material()
        continue_calculating_heat = False
        for y in range(1, self.ROWS + 1):
            for x in range(1, self.COLUMNS + 1):
                r = self.ROWS - y
                c = self.COLUMNS - x

                if self.calculate_heat:
                    if self.heat_map[r][c] != self.base_temp:
                        continue_calculating_heat = True
                    # heat
                    if r + 1 < self.ROWS and self.heat_map[r + 1][c] > self.heat_map[r][c]:
                        diff = self.heat_map[r + 1][c] - self.heat_map[r][c]
                        self.heat_map[r + 1][c] -= diff // 2
                        self.heat_map[r][c] += diff // 2
                        # print(self.heat_map[r][c])
                    if r + 1 < self.ROWS and c + 1 < self.COLUMNS and self.heat_map[r + 1][c + 1] > self.heat_map[r][c] and random.randint(0, 100) > self.heat_width:
                        diff = self.heat_map[r + 1][c + 1] - self.heat_map[r][c]
                        self.heat_map[r + 1][c + 1] -= diff // 2
                        self.heat_map[r][c] += diff // 2
                        # print(self.heat_map[r][c])
                    if r + 1 < self.ROWS and c - 1 >= 0 and self.heat_map[r + 1][c - 1] > self.heat_map[r][c] and random.randint(0, 100) > self.heat_width:
                        diff = self.heat_map[r + 1][c - 1] - self.heat_map[r][c]
                        self.heat_map[r + 1][c - 1] -= diff // 2
                        self.heat_map[r][c] += diff // 2
                        # print(self.heat_map[r][c])


                    if r + 1 < self.ROWS and self.heat_map[r + 1][c] < self.heat_map[r][c] and self.map[r + 1][c] != FIRE and ((c + 1 < self.COLUMNS and self.heat_map[r + 1][c + 1] < self.heat_map[r][c] and self.map[r + 1][c + 1] != FIRE) or c + 1 >= self.COLUMNS) and ((c - 1 >= 0 and self.heat_map[r + 1][c - 1] < self.heat_map[r][c] and self.map[r + 1][c - 1] != FIRE) or c - 1 < 0):
                        diff = self.heat_map[r][c] - self.heat_map[r + 1][c]
                        # self.heat_map[r + 1][c] -= diff // 2
                        #print(f'Before: {self.heat_map[r][c]}')
                        self.heat_map[r][c] -= diff / 2
                        #print(f'After: {self.heat_map[r][c]}')

                if self.particles[(c, r)] is not None:
                    try:
                        self.particles[(c, r)].render()
                    except:
                        print("Error rendering")
                elif self.view_heat:
                    if self.heat_map[r][c] != self.base_temp:
                        self.draw_heat(r, c)
                        self.draw_heat(r + 1, c)
                        self.draw_heat(r + 1, c - 1)
                        self.draw_heat(r + 1, c + 1)
                if self.smoke_map[r][c] != 0:
                    self.smoke_particles[(c, r)].render()

        if continue_calculating_heat is False:
            self.calculate_heat = False

        for value in self.particles.values():
            if value is not None:
                value.rendered = False
        for value in self.smoke_particles.values():
            if value is not None:
                value.rendered = False
        #print(self.active_water_particles)
        for button in self.buttons:
            button.render()
        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        display_text = font.render("S A N D B O X", True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)

        if self.active_particles >= self.max_particles:
            self.active_particles = 0
            self.active_metal_particles = 0
            self.active_liquid_particles = 0

            self.map = [[AIR for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
            self.heat_map = [[20 for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
            self.smoke_map = [[0 for _ in range(self.COLUMNS)] for i in range(self.ROWS)]
            self.particles = {}
            self.smoke_particles = {}
            self.place_radius = 1
            for y in range(self.ROWS):
                for x in range(self.COLUMNS):
                    self.particles[(x, y)] = None
                    self.smoke_particles[(x, y)] = None

        random_row = random.randint(0, self.ROWS - 1)

        random_column = None
        iterations = 0
        while random_column == None and iterations < self.COLUMNS:
            random_column = random.randint(0, self.COLUMNS - 2)
            if self.map[random_row][random_column] != 0:
                random_column = None
            iterations += 1
        if random_column is not None:
            has_selected_material = False
            while has_selected_material is False:
                self.selected_material = random.choice(self.materials)
                if self.selected_material in self.METALS:
                    if self.active_metal_particles <= self.max_metal_particles:
                        self.active_metal_particles += 1
                        has_selected_material = True
                elif self.selected_material in self.LIQUIDS:
                    if self.active_liquid_particles <= self.max_liquid_particles:
                        self.active_liquid_particles += 1
                        has_selected_material = True
                else:
                    has_selected_material = True
            self.active_particles += 1
            self.add_material(random_column, random_row)


    # Overrides the default events function in app.py
    def events(self):
        pass
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.app.run = False
        #         pygame.quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_1:
        #             self.selected_material = SAND
        #         if event.key == pygame.K_2:
        #             self.selected_material = WATER
        #         if event.key == pygame.K_3:
        #             self.selected_material = STONE
        #         if event.key == pygame.K_4:
        #             self.selected_material = ACID
        #         if event.key == pygame.K_5:
        #             self.selected_material = PLASTIC
        #         if event.key == pygame.K_6:
        #             self.selected_material = FIRE
        #         if event.key == pygame.K_7:
        #             self.selected_material = OIL
        #         if event.key == pygame.K_8:
        #             self.selected_material = IRON
        #         if event.key == pygame.K_9:
        #             self.selected_material = GOLD
        #         if event.key == pygame.K_0:
        #             self.selected_material = COPPER
        #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #         self.add_material_on = True
        #     if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        #         self.add_material_on = False

    def add_material(self, x, y):
        clicked_row = y
        clicked_column = x
        if clicked_column >= self.COLUMNS or clicked_row >= self.ROWS:
            return
        # if self.map[clicked_row][clicked_column] == self.selected_material:
        #     return
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
                    try:
                        self.map[y][x] = self.selected_material
                        self.particles[(x, y)] = stone.StoneParticle(self, x, y, (136, 140, 141))
                    except:
                        pass

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
                    try:
                        self.map[y][x] = self.selected_material
                        self.particles[(x, y)] = plastic.PlasticParticle(self, x, y, (215, 215, 215))
                    except:
                        pass

        if self.selected_material == FIRE:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    try:
                        self.map[y][x] = self.selected_material
                        self.particles[(x, y)] = fire.FireParticle(self, x, y, self.bg_color)
                        self.calculate_heat = True
                    except:
                        pass
        if self.selected_material == OIL:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    if random.randint(0, 100) > 10:
                        try:
                            self.map[y][x] = self.selected_material
                            self.particles[(x, y)] = oil.OilParticle(self, x, y, (69, 45, 19))
                        except:
                            pass
        if self.selected_material == IRON:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    try:
                        self.map[y][x] = self.selected_material
                        self.particles[(x, y)] = metal.MetalParticle(self, x, y, (188, 196, 204), 150, 20)
                    except:
                        pass
        if self.selected_material == GOLD:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    try:
                        self.map[y][x] = self.selected_material
                        self.particles[(x, y)] = metal.MetalParticle(self, x, y, (212, 175, 55), 90, 20)
                    except:
                        pass
        if self.selected_material == COPPER:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    try:
                        self.map[y][x] = self.selected_material
                        self.particles[(x, y)] = metal.MetalParticle(self, x, y, (184, 115, 51), 100, 20)
                    except:
                        pass
        if self.selected_material == HYDROGEN:
            #self.particles[(clicked_column, clicked_row)] = sand.SandParticle(self, clicked_column, clicked_row, (230, 200, 0), 0)
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    if random.randint(0, 100) > 65:
                        try:
                            self.map[y][x] = self.selected_material
                            self.particles[(x, y)] = smoke.SmokeParticle(self, x, y, 'H2')
                        except:
                            pass
        if self.selected_material == CHLORINE:
            #self.particles[(clicked_column, clicked_row)] = sand.SandParticle(self, clicked_column, clicked_row, (230, 200, 0), 0)
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    if random.randint(0, 100) > 65:
                        try:
                            self.map[y][x] = self.selected_material
                            self.particles[(x, y)] = chlorine.ChlorineParticle(self, x, y, (255, 255, 255), 25)
                        except:
                            pass
        if self.selected_material == 0:
            for y in range(clicked_row - self.place_radius, clicked_row + self.place_radius + 1):
                for x in range(clicked_column - self.place_radius, clicked_column + self.place_radius + 1):
                    try:
                        self.map[y][x] = 0
                        self.particles[(x, y)] = None
                        self.smoke_map[y][x] = 0
                        self.smoke_particles[(x, y)] = None
                    except:
                        pass