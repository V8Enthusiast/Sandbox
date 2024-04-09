import pygame
from classes import buttons

class Settings:
    def __init__(self, app):
        self.app = app
        self.main_text_rect_center = (self.app.width // 2, 250 * self.app.scale)
        self.font = "fonts/main_font.ttf"
        self.font_color = (255, 255, 255)
        self.buttons = [buttons.Button(200 * self.app.scale, 75 * self.app.scale, self.app.width/2 - 100 * self.app.scale, self.app.height/2 - 75 * self.app.scale/2, False, "fonts/main_font.ttf", "Back", (0, 0, 0), (255, 255, 255), 'back', self.app)]

    def render(self):
        self.app.screen.fill((127, 127, 127))
        for button in self.buttons:
            button.render()
        font = pygame.font.Font(self.font, int(72 * self.app.scale))
        display_text = font.render("COMING SOON...", True, self.font_color)
        display_text_rect = display_text.get_rect()
        display_text_rect.center = self.main_text_rect_center
        self.app.screen.blit(display_text, display_text_rect)

    def events(self):
        pass