import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Running Through The City")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load("../data/images/clouds/clouds1.png")

    def run(self):
        while True:
            self.screen.blit(self.img, (100, 200))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

Game().run()