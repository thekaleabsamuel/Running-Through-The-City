import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Running Through The City")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        # Load and resize the image
        img = pygame.image.load("/Users/donjuan/Downloads/data/images/clouds/file.png")
        self.img = pygame.transform.scale(img, (75, 75))

        # Load the background images
        bg_img = pygame.image.load("/Users/donjuan/Downloads/data/images/_7d090ca7-6057-4bb4-9f5e-412846be2ca9.jpeg")
        bg_img = pygame.transform.scale(bg_img, (640, 480))  # Resize the image to fit the screen
        self.bg_imgs = [bg_img, bg_img]
        self.bg_pos = [[0, 0], [bg_img.get_width(), 0]]

        self.img_pos = [160, 260]
        self.movement = [False, False, False, False]  # Up, Down, Left, Right

        self.collision_areas = pygame.Rect(50, 50, 300, 50)

    def run(self):
        while True:
            self.screen.fill((14,219,248))

            # Move and draw the background images
            for i in range(2):
                self.bg_pos[i][0] -= 1  # Move to the left
                if self.bg_pos[i][0] < -self.bg_imgs[i].get_width():
                    self.bg_pos[i][0] = self.bg_imgs[i].get_width()  # Reset position to the right
                self.screen.blit(self.bg_imgs[i], self.bg_pos[i])

            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
            self.img_pos[0] += (self.movement[3] - self.movement[2]) * 5  # Left and Right movement

            self.screen.blit(self.img , self.img_pos)

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            
            # Check for collision
            if img_r.colliderect(self.collision_areas):
                print("Collision detected!")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:  # Added left movement
                        self.movement[2] = True
                    if event.key == pygame.K_RIGHT:  # Added right movement
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:  # Added left movement
                        self.movement[2] = False
                    if event.key == pygame.K_RIGHT:  # Added right movement
                        self.movement[3] = False

            pygame.display.update()
            self.clock.tick(60)

Game().run()