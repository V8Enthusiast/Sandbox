import pygame
import random
import functions

acid_strength = 25
max_acid_strength = 50
ACID = 4

class AcidParticle:
    def __init__(self, simulation, x, y, color):
        self.simulation = simulation # a reference to the parent class (needed to access f.e. screen, map and particle size)
        self.x = x
        self.y = y
        self.color = color
        self.rendered = False
        self.isFalling = True
        self.strength = acid_strength
        self.liquid_neighbour_count = 0 # amount of liquid particles neighbouring with the particle which have less strength than the current particle
        self.avg_neighbour_strength = 0

    def render(self):
        if self.rendered is False:
            print(self.strength)
            #self.color = (int(176 * self.strength / max_acid_strength), int(191 * self.strength / max_acid_strength), int(26 * self.strength / max_acid_strength))
            self.color = functions.mix_colors((0, 255, 0), (90, 188, 216), self.strength/max_acid_strength) # color 1 is acid, color 2 is water
            rect = pygame.Rect(0, 0, self.simulation.particle_size, self.simulation.particle_size)
            rect.center = (self.x * self.simulation.particle_size, self.y * self.simulation.particle_size)
            pygame.draw.rect(self.simulation.window, self.color, rect)
            self.calculate_physics()
            self.rendered = True
            self.simulation.active_water_particles += 1

    def update_liquid_neighbour_count(self):
        self.liquid_neighbour_count = 0
        self.avg_neighbour_strength = 0
        # above particle
        if self.y - 1 >= 0 and self.simulation.map[self.y - 1][self.x] in self.simulation.LIQUIDS and self.simulation.particles[(self.x, self.y - 1)].strength < self.strength:
            self.liquid_neighbour_count += 1
            self.avg_neighbour_strength += self.simulation.particles[(self.x, self.y - 1)].strength
            if self.x - 1 >= 0 and self.simulation.map[self.y - 1][self.x - 1] in self.simulation.LIQUIDS and self.simulation.particles[(self.x - 1, self.y - 1)].strength < self.strength:
                self.liquid_neighbour_count += 1
                self.avg_neighbour_strength += self.simulation.particles[(self.x - 1, self.y - 1)].strength
            if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y - 1][self.x + 1] in self.simulation.LIQUIDS and self.simulation.particles[(self.x + 1, self.y - 1)].strength < self.strength:
                self.liquid_neighbour_count += 1
                self.avg_neighbour_strength += self.simulation.particles[(self.x + 1, self.y - 1)].strength
        # on the same level as particle
        if self.x - 1 >= 0 and self.simulation.map[self.y][self.x - 1] in self.simulation.LIQUIDS and self.simulation.particles[(self.x - 1, self.y)].strength < self.strength:
            self.liquid_neighbour_count += 1
            self.avg_neighbour_strength += self.simulation.particles[(self.x - 1, self.y)].strength
        if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y][self.x + 1] in self.simulation.LIQUIDS and self.simulation.particles[(self.x + 1, self.y)].strength < self.strength:
            self.liquid_neighbour_count += 1
            self.avg_neighbour_strength += self.simulation.particles[(self.x + 1, self.y)].strength
        # below particle
        if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] in self.simulation.LIQUIDS and self.simulation.particles[(self.x, self.y + 1)].strength < self.strength:
            self.liquid_neighbour_count += 1
            self.avg_neighbour_strength += self.simulation.particles[(self.x, self.y + 1)].strength
            if self.x - 1 >= 0 and self.simulation.map[self.y + 1][self.x - 1] in self.simulation.LIQUIDS and self.simulation.particles[(self.x - 1, self.y + 1)].strength < self.strength:
                self.liquid_neighbour_count += 1
                self.avg_neighbour_strength += self.simulation.particles[(self.x - 1, self.y + 1)].strength
            if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y + 1][self.x + 1] in self.simulation.LIQUIDS and self.simulation.particles[(self.x + 1, self.y + 1)].strength < self.strength:
                self.liquid_neighbour_count += 1
                self.avg_neighbour_strength += self.simulation.particles[(self.x + 1, self.y + 1)].strength

        self.avg_neighbour_strength += self.strength
        self.avg_neighbour_strength /= self.liquid_neighbour_count + 1

    def replace_particle_with_acid(self, x, y, strength_increment):
        self.simulation.map[y][x] = ACID
        self.simulation.particles[(x, y)] = AcidParticle(self.simulation, x, y,(0, 255, 0))
        self.simulation.particles[(x, y)].strength = strength_increment
        self.strength -= strength_increment # remove the strength given to the particle from self

    def add_acid_strength_to_particle(self, x, y, strength_increment, avg_strength):
        if self.simulation.particles[(x, y)].strength + strength_increment > avg_strength:
            strength_increment = avg_strength - self.simulation.particles[(x, y)].strength
            if strength_increment < 0:
                strength_increment = 0
            self.simulation.particles[(x, y)].strength = avg_strength
        else:
            self.simulation.particles[(x, y)].strength += strength_increment
        self.strength -= strength_increment # remove the strength given to the particle from self

    def calculate_physics(self):
        # checks if at least one particle under is air
        if self.y + 1 < self.simulation.ROWS and ((self.simulation.map[self.y + 1][self.x] == 0 or self.simulation.particles[(self.x, self.y + 1)].isFalling) or (self.x + 1 < self.simulation.COLUMNS and (self.simulation.map[self.y + 1][self.x + 1] == 0 or self.simulation.particles[(self.x + 1, self.y + 1)].isFalling)) or (self.x - 1 >= 0 and (self.simulation.map[self.y + 1][self.x - 1] == 0 or self.simulation.particles[(self.x - 1, self.y + 1)].isFalling))):
            self.isFalling = True
        # checks if the particle is covered by a liquid
        if self.y - 1 >= 0 and (self.simulation.map[self.y - 1][self.x] not in self.simulation.LIQUIDS or (self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y - 1][self.x + 1] == 0) or (self.x - 1 >= 0 and self.simulation.map[self.y - 1][self.x - 1] == 0)):
            self.isFalling = True
        if self.isFalling:
            if random.randint(0, 100) <= self.strength:
                isDissolving = True
            else:
                isDissolving = False
            # if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] in self.simulation.NON_DISSOLVABLE_PARTICLES and self.simulation.particles[(self.x, self.y + 1)].isFalling is False:
            #     self.isFalling = False
            if self.y - 1 >= 0 and self.simulation.map[self.y - 1][self.x] != 0 and self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y - 1][self.x + 1] != 0 and self.x - 1 >= 0 and self.simulation.map[self.y - 1][self.x - 1] != 0:
                self.isFalling = False
                self.update_liquid_neighbour_count()
                #self.color = (255, 255, 255)
            elif self.y + 1 >= self.simulation.ROWS:
                self.isFalling = False
                self.update_liquid_neighbour_count()
            # else:
            #     self.color = (176, 191, 26)

            if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] != 0 and self.isFalling and (isDissolving is False or self.simulation.map[self.y + 1][self.x] in self.simulation.NON_DISSOLVABLE_PARTICLES): # particle under is a not air

                # to the right
                first_empty_particle_right_x = None
                for i in range(1, self.simulation.COLUMNS - self.x):
                    if self.simulation.map[self.y + 1][self.x + i] == 0:
                        first_empty_particle_right_x = self.x + i
                        break
                    if self.simulation.map[self.y + 1][self.x + i] in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS:
                        break

                # to the left
                first_empty_particle_left_x = None
                for n in range(1, self.x):
                    if self.simulation.map[self.y + 1][self.x - n] == 0:
                        first_empty_particle_left_x = self.x - n
                        break
                    if self.simulation.map[self.y + 1][self.x - n] in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS:
                        break

                if first_empty_particle_left_x is not None and first_empty_particle_right_x is not None: # if acid can flow to both sides choose only one
                    if abs(self.x - first_empty_particle_left_x) == abs(self.x - first_empty_particle_right_x):
                        if random.randint(0, 100) >= 50:
                            first_empty_particle_left_x = None
                        else:
                            first_empty_particle_right_x = None
                    else:
                        if abs(self.x - first_empty_particle_left_x) < abs(self.x - first_empty_particle_right_x): # left is closer
                            first_empty_particle_right_x = None
                        else:
                            first_empty_particle_left_x = None

                if first_empty_particle_left_x is not None:
                    self.simulation.map[self.y][self.x] = 0  # reset the current square
                    self.simulation.map[self.y + 1][first_empty_particle_left_x] = 4  # add the acid to the chosen square
                    self.simulation.particles[(self.x, self.y)] = None
                    self.simulation.particles[(first_empty_particle_left_x, self.y + 1)] = self
                    self.y += 1
                    self.x = first_empty_particle_left_x

                if first_empty_particle_right_x is not None:
                    self.simulation.map[self.y][self.x] = 0  # reset the current square
                    self.simulation.map[self.y + 1][first_empty_particle_right_x] = 4  # add the acid to the chosen square
                    self.simulation.particles[(self.x, self.y)] = None
                    self.simulation.particles[(first_empty_particle_right_x, self.y + 1)] = self
                    self.y += 1
                    self.x = first_empty_particle_right_x

            elif self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] not in self.simulation.SOLIDS + self.simulation.MOVING_SOLIDS + self.simulation.LIQUIDS: # acid is on top of air
                self.simulation.map[self.y][self.x] = 0 # reset the current square
                self.simulation.map[self.y + 1][self.x] = 4
                self.simulation.particles[(self.x, self.y)] = None
                self.simulation.particles[(self.x, self.y + 1)] = self
                self.y += 1
            elif self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] not in self.simulation.NON_DISSOLVABLE_PARTICLES and isDissolving:
                print(self.simulation.map[self.y + 1][self.x])
                self.simulation.map[self.y][self.x] = 0 # reset the current square
                self.simulation.map[self.y + 1][self.x] = 4
                self.simulation.particles[(self.x, self.y)] = None
                self.simulation.particles[(self.x, self.y + 1)] = self
                self.y += 1
        self.update_liquid_neighbour_count()
        if self.liquid_neighbour_count > 0:
            avg_strength = self.avg_neighbour_strength
            strength_increment = (self.strength - avg_strength) / (self.liquid_neighbour_count + 1)

            # particles above self
            if self.y - 1 >= 0:

                # particle above is less acidic than self
                if self.simulation.map[self.y - 1][self.x] in self.simulation.NON_ACIDIC_LIQUIDS:
                    # replace the particle with acid
                    self.replace_particle_with_acid(self.x, self.y - 1, strength_increment)
                elif self.simulation.map[self.y - 1][self.x] == ACID and self.simulation.particles[(self.x, self.y - 1)].strength < avg_strength:
                    # add strength to the acid at that square
                    self.add_acid_strength_to_particle(self.x, self.y - 1, strength_increment, avg_strength)

                # particle to the left and up is less acidic than self
                if self.x - 1 >= 0 and self.simulation.map[self.y - 1][self.x - 1] in self.simulation.NON_ACIDIC_LIQUIDS:
                    # replace the particle with acid
                    self.replace_particle_with_acid(self.x - 1, self.y - 1, strength_increment)
                elif self.x - 1 >= 0 and self.simulation.map[self.y - 1][self.x - 1] == ACID and self.simulation.particles[(self.x - 1, self.y - 1)].strength < avg_strength:
                    # add strength to the acid at that square
                    self.add_acid_strength_to_particle(self.x - 1, self.y - 1, strength_increment, avg_strength)

                # particle to the right and up is less acidic than self
                if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y - 1][self.x + 1] in self.simulation.NON_ACIDIC_LIQUIDS:
                    # add strength to the acid at that square
                    self.replace_particle_with_acid(self.x + 1, self.y - 1, strength_increment)
                elif self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y - 1][self.x + 1] == ACID and self.simulation.particles[(self.x + 1, self.y - 1)].strength < avg_strength:
                    # add strength to the acid at that square
                    self.add_acid_strength_to_particle(self.x + 1, self.y - 1, strength_increment, avg_strength)


            # particles on the same y-level as self

            # particle to the left is less acidic than self
            if self.x - 1 >= 0 and self.simulation.map[self.y][self.x - 1] in self.simulation.NON_ACIDIC_LIQUIDS:
                # replace the particle with acid
                self.replace_particle_with_acid(self.x - 1, self.y, strength_increment)
            elif self.x - 1 >= 0 and self.simulation.map[self.y][self.x - 1] == ACID and self.simulation.particles[(self.x - 1, self.y)].strength < avg_strength:
                # add strength to the acid at that square
                self.add_acid_strength_to_particle(self.x - 1, self.y, strength_increment, avg_strength)

            # particle to the right is less acidic than self
            if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y][self.x + 1] in self.simulation.NON_ACIDIC_LIQUIDS:
                # add strength to the acid at that square
                self.replace_particle_with_acid(self.x + 1, self.y, strength_increment)
            elif self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y][self.x + 1] == ACID and self.simulation.particles[(self.x + 1, self.y)].strength < avg_strength:
                # add strength to the acid at that square
                self.add_acid_strength_to_particle(self.x + 1, self.y, strength_increment, avg_strength)

            # particles under self
            if self.y + 1 < self.simulation.ROWS:

                # particle under is less acidic than self
                if self.simulation.map[self.y + 1][self.x] in self.simulation.NON_ACIDIC_LIQUIDS:
                    # replace the particle with acid
                    self.replace_particle_with_acid(self.x, self.y + 1, strength_increment)
                elif self.simulation.map[self.y + 1][self.x] == ACID and self.simulation.particles[(self.x, self.y + 1)].strength < avg_strength:
                    # add strength to the acid at that square
                    self.add_acid_strength_to_particle(self.x, self.y + 1, strength_increment, avg_strength)

                # particle to the left and down is less acidic than self
                if self.x - 1 >= 0 and self.simulation.map[self.y + 1][self.x - 1] in self.simulation.NON_ACIDIC_LIQUIDS:
                    # replace the particle with acid
                    self.replace_particle_with_acid(self.x - 1, self.y + 1, strength_increment)
                elif self.x - 1 >= 0 and self.simulation.map[self.y + 1][self.x - 1] == ACID and self.simulation.particles[(self.x - 1, self.y + 1)].strength < avg_strength:
                    # add strength to the acid at that square
                    self.add_acid_strength_to_particle(self.x - 1, self.y + 1, strength_increment, avg_strength)

                # particle to the right and down is less acidic than self
                if self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y + 1][self.x + 1] in self.simulation.NON_ACIDIC_LIQUIDS:
                    # add strength to the acid at that square
                    self.replace_particle_with_acid(self.x + 1, self.y + 1, strength_increment)
                elif self.x + 1 < self.simulation.COLUMNS and self.simulation.map[self.y + 1][self.x + 1] == ACID and self.simulation.particles[(self.x + 1, self.y + 1)].strength < avg_strength:
                    # add strength to the acid at that square
                    self.add_acid_strength_to_particle(self.x + 1, self.y + 1, strength_increment, avg_strength)




        if self.y + 1 < self.simulation.ROWS and self.simulation.map[self.y + 1][self.x] not in self.simulation.NON_DISSOLVABLE_PARTICLES:
            if random.randint(0, 100) <= self.strength:
                print(self.simulation.map[self.y + 1][self.x])
                self.simulation.map[self.y][self.x] = 0  # reset the current square
                self.simulation.map[self.y + 1][self.x] = 4
                self.simulation.particles[(self.x, self.y)] = None
                self.simulation.particles[(self.x, self.y + 1)] = self
                self.y += 1