from player import Player
from themes import THEMES
import game

def main():
    while True:
        if input("Start game? (y/n) ").lower() == "y":
            game.players.clear()
            game.board.clear()
            while len(game.players) < 4:
                name = input(f"Player {len(game.players) + 1} single-character token (or press Enter to start): ")
                if not name and len(game.players) >= 2:
                    break
                elif len(name) == 1 and name not in [p.name for p in game.players]:
                    game.players.append(Player(name, 1500))
                else:
                    print("You need at least 2 players with unique 1-character names.")
            while True:
                print("Select board theme:")
                for i, theme in enumerate(THEMES):
                    print(f"{i + 1}. {theme['name']} - {theme['description']}")
                choice = input("Choice: ")
                if choice.isdigit() and 1 <= int(choice) <= len(THEMES):
                    theme_data = THEMES[int(choice) - 1]
                    game.board.extend(theme_data['map'])
                    break
                else:
                    print(f"Invalid choice. Please select 1 through {len(THEMES)}.")
            for index, tile in enumerate(game.board):
                tile.index = index
                if hasattr(tile, 'owner'):
                    tile.owner = None
                if hasattr(tile, 'houses'):
                    tile.houses = 0
                if hasattr(tile, 'group') and tile.group in theme_data:
                    tile.cards = theme_data[tile.group]
            game_over = False
            while not game_over:
                for player in game.players.copy():
                    if player.money < 0:
                        print(f"\n{player.name} is bankrupt and eliminated from the game!")
                        for item in player.inventory:
                            item.owner = None
                            if hasattr(item, 'houses'):
                                item.houses = 0
                        player.bankrupt = True
                        player.inventory.clear()
                        player.position = -1
                        
                        active_players = [p for p in game.players if not getattr(p, 'bankrupt', False)]
                        if len(active_players) == 1:
                            print(f"\n🎉 {active_players[0].name} HAS WON THE GAME WITH ${active_players[0].money}! 🎉")
                            game_over = True
                            break
                        continue

                    if not getattr(player, 'bankrupt', False):
                        player.turn()
        else:
            print("Exiting game.")
            break

if __name__ == "__main__":
    main()