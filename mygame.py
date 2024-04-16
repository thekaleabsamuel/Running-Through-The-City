import sys
import pygame
import random
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Running Through The City")
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load('/Users/donjuan/Downloads/data/RUNNIN 8BIT.mp3')  # Load the music file
        pygame.mixer.music.play(-1)  # Play the music, -1 means loop indefinitely
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Create a Font object


        # Load and resize the main character
        img = pygame.image.load("/Users/donjuan/Downloads/data/Screen_Shot_2024-04-12_at_8.23.32_PM-removebg-preview.png")
        self.img = pygame.transform.scale(img, (100, 75))

        # Load and resize the coin image
        coin_img = pygame.image.load("/Users/donjuan/Downloads/data/images/_55c73e18-c0b8-4460-bbb9-c0d34730aa1d-removebg-preview.png")
        self.coin_img = pygame.transform.scale(coin_img, (50, 50))  # Resize the coin image

        # Load and resize the enemy image
        enemy_img = pygame.image.load("/Users/donjuan/Downloads/data/images/entities/player/run/_a062e3da-97e8-4fce-9bcd-4c22debebdac-removebg-preview (2).png")
        self.enemy_img = pygame.transform.scale(enemy_img, (75, 75))  # Resize the enemy image

        # Initialize the enemies
        self.enemies = [[640, 200]]  # Start off the screen and at a fixed y position

        # Load the background images
        bg_img = pygame.image.load("/Users/donjuan/Downloads/data/images/_0dc7c597-8560-44a6-a167-735d573c229e.jpeg")
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


        
class GameCharacter:
    def __init__(self, name, image_path):
        self.name = name
        self.image = pygame.image.load(image_path)

class CharacterSelection:
    def __init__(self, screen):
        self.screen = screen
        self.characters = [
            GameCharacter('Character1', '/Users/donjuan/Downloads/data/images/Screen_Shot_2024-04-12_at_7.29.48_PM-removebg-preview.png'),
            GameCharacter('Character2', '/Users/donjuan/Downloads/data/Screen_Shot_2024-04-12_at_8.23.32_PM-removebg-preview.png'),
            GameCharacter('Character3', '/Users/donjuan/Downloads/data/images/Screen_Shot_2024-04-12_at_7.19.35_PM-removebg-preview.png'),
        ]
        self.selected_character = None

    def display(self):
        for i, character in enumerate(self.characters, start=1):
            print(f"{i}. {character.name}")
            # Display the character image on the screen
            # You would need to adjust the position and size to fit your game
            self.screen.blit(pygame.transform.scale(character.image, (100, 100)), (i * 120, 200))

        character_choice = int(input("Enter the number of your choice: "))
        self.selected_character = self.characters[character_choice - 1]

    def get_selected_character(self):
        return self.selected_character


    def run(self):
        while True:
            self.screen.fill((14,219,248))

            # Move and draw the background images
            for i in range(2):
                self.bg_pos[i][0] -= 1  # Move to the left
                if self.bg_pos[i][0] < -self.bg_imgs[i].get_width():
                    self.bg_pos[i][0] = self.bg_imgs[i].get_width()  # Reset position to the right
                self.screen.blit(self.bg_imgs[i], self.bg_pos[i])


            # Move and draw the enemies
            for enemy in self.enemies:
                enemy[0] -= 2  # Move to the left faster than the background
                if enemy[0] < -self.enemy_img.get_width():
                    enemy[0] = 640  # Reset position to the right
                    enemy[1] = random.randint(100, 400)  # Randomize the y position
                self.screen.blit(self.enemy_img, enemy)


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

             # Render the score text
            score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
            self.screen.blit(score_text, (500, 10))  # Draw the score text onto the screen

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
                    self.score += 10  # Increase the score
                    print("Score:", self.score)  # Print the current score

            # Check for collision with enemies
            for enemy in self.enemies:
                if img_r.colliderect(pygame.Rect(enemy[0], enemy[1], self.enemy_img.get_width(), self.enemy_img.get_height())):
                    print("Game over!")
                    self.__init__()  # Restart the game
                    break  # Break out of the loop to avoid modifying the list while iterating


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
            pygame.K_UP: 0,
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
            pygame.K_UP: 0,
            pygame.K_DOWN: 1,
            pygame.K_LEFT: 2,
            pygame.K_RIGHT: 3
        }

        if event.key in key_to_movement_index:
            self.movement[key_to_movement_index[event.key]] = False

        # If the up arrow key is released, stop the upward movement
        if event.key == pygame.K_UP:
            self.movement[0] = False


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    _name = Column('name', String)
    high_score = Column(Integer, default=0)  # Add a high_score field
    games = relationship('GameRecord', backref='player')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Player name cannot be empty.")
        self._name = value

    @classmethod
    def update_high_score(cls, id, score):
        player = session.query(cls).get(id)
        if player and score > player.high_score:
            player.high_score = score
            session.commit()

    @classmethod
    def create(cls, name):
        player = cls(name=name)
        session.add(player)
        session.commit()
        return player

    @classmethod
    def delete(cls, id):
        player = session.query(cls).get(id)
        if player:
            session.delete(player)
            session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).get(id)

class GameRecord(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    player_id = Column(Integer, ForeignKey('players.id'))

    @classmethod
    def create(cls, score, player_id):
        game = cls(score=score, player_id=player_id)
        session.add(game)
        session.commit()
        return game

    @classmethod
    def delete(cls, id):
        game = session.query(cls).get(id)
        if game:
            session.delete(game)
            session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).get(id)

def main_menu():
    print("1. Start Game")
    print("2. Create Player")
    print("3. Delete Player")
    print("4. Display All Players")
    print("5. Create Game")
    print("6. Delete Game")
    print("7. Display All Games")
    print("8. Exit")
    choice = input("Choose an option: ")
    return choice

def create_player():
    name = input("Enter player name: ")
    if not name:
        print("Player name cannot be empty.")
        return
    Player.create(name=name)

def delete_player():
    id = input("Enter player id: ")
    Player.delete(id)

def display_all_players():
    players = Player.get_all()
    for player in players:
        print(f"ID: {player.id}, Name: {player.name}")

def create_game():
    score = input("Enter game score: ")
    player_id = input("Enter player id: ")
    GameRecord.create(score=score, player_id=player_id)

def delete_game():
    id = input("Enter game id: ")
    GameRecord.delete(id)

def display_all_games():
    games = GameRecord.get_all()
    for game in games:
        print(f"ID: {game.id}, Score: {game.score}, Player ID: {game.player_id}")

def main():
    while True:
        choice = main_menu()
        if choice == "1":
            game = Game()
            character_selection = CharacterSelection(game.screen)
            character_selection.display()
            selected_character = character_selection.get_selected_character()
            game.character = selected_character
            game.run()
        # elif choice == "3":
        #     display_all_players()
        # elif choice == "4":
        #     create_game()
        # elif choice == "5":
        #     delete_game()
        # elif choice == "6":
        #     display_all_games()
        # elif choice == "7":
        #     break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()

# Create a new player
new_player = Player.create(name='John Doe')

# Create a new game for this player
new_game = GameRecord.create(score=100, player_id=new_player.id)

# Query all players
players = Player.get_all()
for player in players:
    print(player.name)

# Query all games of a player
games = session.query(GameRecord).filter(GameRecord.player_id == new_player.id).all()
for game in games:
    print(game.score)

Game().run()