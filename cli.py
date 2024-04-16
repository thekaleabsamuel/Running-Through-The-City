# from mygame import Player, Game, session

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
    Game.create(score=score, player_id=player_id)

def delete_game():
    id = input("Enter game id: ")
    Game.delete(id)

def display_all_games():
    games = Game.get_all()
    for game in games:
        print(f"ID: {game.id}, Score: {game.score}, Player ID: {game.player_id}")

def main():
    while True:
        choice = main_menu()
        if choice == "1":
            create_player()
        elif choice == "2":
            delete_player()
        elif choice == "3":
            display_all_players()
        elif choice == "4":
            create_game()
        elif choice == "5":
            delete_game()
        elif choice == "6":
            display_all_games()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()