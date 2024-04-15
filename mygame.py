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

        # Load and resize the coin image
        coin_img = pygame.image.load("/Users/donjuan/Downloads/data/images/_55c73e18-c0b8-4460-bbb9-c0d34730aa1d-removebg-preview.png")
        self.coin_img = pygame.transform.scale(coin_img, (50, 50))  # Resize the coin image

        # Load the background images
        bg_img = pygame.image.load("/Users/donjuan/Downloads/data/images/Screen Shot 2024-04-15 at 11.00.29 AM.png")
        bg_img = pygame.transform.scale(bg_img, (640, 480))  # Resize the image to fit the screen
        self.bg_imgs = [bg_img, bg_img]
        self.bg_pos = [[0, 0], [bg_img.get_width(), 0]]


        self.img_pos = [160, 260]
        self.movement = [False, False, False, False]  # Up, Down, Left, Right
        self.score = 0  # Initialize the score


        self.collision_areas = pygame.Rect(50, 50, 300, 50)
        self.gravity = 1  # The strength of gravity
        self.vertical_speed = 0  # The vertical speed of the character
        self.jump_strength = 15  # Increase this value for a higher jump
        self.coins = [[640, y] for y in range(100, 401, 100)]  # Start off the screen and at different y positions


        

    def run(self):
        while True:
            self.screen.fill((14,219,248))

            # Move and draw the background images
            for i in range(2):
                self.bg_pos[i][0] -= 1  # Move to the left
                if self.bg_pos[i][0] < -self.bg_imgs[i].get_width():
                    self.bg_pos[i][0] = self.bg_imgs[i].get_width()  # Reset position to the right
                self.screen.blit(self.bg_imgs[i], self.bg_pos[i])

            # Check for collision with coins        
            for coin in self.coins:
                if img_r.colliderect(pygame.Rect(coin[0], coin[1], self.coin_img.get_width(), self.coin_img.get_height())):
                    print("Coin collected!")
                    coin[0] = 640  # Reset position to the right
                    self.score += 10  # Increase the score
                    print("Score:", self.score)  # Print the current score

            # Move and draw the coins
            for coin in self.coins:
                coin[0] -= 1  # Move to the left
                if coin[0] < -self.coin_img.get_width():
                    coin[0] = 640  # Reset position to the right
                self.screen.blit(self.coin_img, coin)

            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
            self.img_pos[0] += (self.movement[3] - self.movement[2]) * 5  # Left and Right movement
            self.vertical_speed += self.gravity
            self.img_pos[1] += self.vertical_speed

            # Check if character has reached the ground
            if self.img_pos[1] >= 400:
                self.img_pos[1] = 400
                self.vertical_speed = 0

            self.screen.blit(self.img , self.img_pos)

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            
            # Check for collision with coins
            for coin in self.coins:
                if img_r.colliderect(pygame.Rect(coin[0], coin[1], self.coin_img.get_width(), self.coin_img.get_height())):
                    print("Coin collected!")
                    coin[0] = 640  # Reset position to the right

            # Check for collision with collision areas
            if img_r.colliderect(self.collision_areas):
                print("Collision detected!")

            for event in pygame.event.get():
                self.handle_event(event)

            pygame.display.update()
            self.clock.tick(60)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)

        if event.type == pygame.KEYUP:
            self.handle_keyup(event)

    def handle_keydown(self, event):
        key_to_movement_index = {
            pygame.K_DOWN: 1,
            pygame.K_LEFT: 2,
            pygame.K_RIGHT: 3
        }

        if event.key in key_to_movement_index:
            self.movement[key_to_movement_index[event.key]] = True

        # If the up arrow key is pressed and the character is on the ground, make the character jump
        if event.key == pygame.K_UP and self.img_pos[1] >= 400:
            self.vertical_speed = -self.jump_strength
            self.movement[0] = True

    def handle_keyup(self, event):
        key_to_movement_index = {
            pygame.K_DOWN: 1,
            pygame.K_LEFT: 2,
            pygame.K_RIGHT: 3
        }

        if event.key in key_to_movement_index:
            self.movement[key_to_movement_index[event.key]] = False

        # If the up arrow key is released, stop the upward movement
        if event.key == pygame.K_UP:
            self.movement[0] = False

Game().run()