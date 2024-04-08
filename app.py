import pygame
from classes import mainmenu

class App:
    def __init__(self, width, height, fullscreen, vsync):
        # Save the data passed into the function to variables
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.width = width
        self.height = height
        self.is_FS_enabled = fullscreen
        self.is_vsync_enabled = vsync
        self.scale = 1

        self.hotbar_height = 100 * self.scale
        self.ui = mainmenu.MainMenu(self)
        self.isUserMovingPiece = False

        # Initialize pygame
        pygame.init()

        # Window setup
        if fullscreen:
            self.screen = pygame.display.set_mode((width, height + self.hotbar_height), pygame.FULLSCREEN, vsync=int(vsync))
        else:
            self.screen = pygame.display.set_mode((width, height + self.hotbar_height), vsync=int(vsync))

        self.run = True # Variable to determine if the app is running
        pygame.display.set_caption("Sandbox")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_pos = pygame.mouse.get_pos()
                for button in self.ui.buttons:
                    if button.rect.collidepoint(click_pos[0], click_pos[1]):
                        button.click()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                print(pygame.mouse.get_pos())


    def background(self):
        self.screen.fill((0, 0, 0))

    def update(self):
        pygame.display.update()
    def mainloop(self):
        self.clock.tick(self.fps)
        #print(self.clock.get_fps())
        if self.run is False:
            pygame.quit()
        self.background()
        self.ui.render()
        self.update()
        self.ui.events()
        self.events()
