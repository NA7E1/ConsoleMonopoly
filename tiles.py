import textwrap
import random
import game

COLORS = {
    "Brown": "\033[38;5;94m",
    "Light Blue": "\033[38;5;117m",
    "Pink": "\033[38;5;218m",
    "Orange": "\033[38;5;208m",
    "Red": "\033[38;5;196m",
    "Yellow": "\033[38;5;226m",
    "Green": "\033[38;5;40m",
    "Dark Blue": "\033[38;5;21m"
}

class Tile:
    def __init__(self, name):
        self.name = name

    def tile(self):
        lines = textwrap.wrap(self.name, 11)[:2]
        players_on_tile = [p.name for p in game.players if getattr(p, 'position', -1) == getattr(self, 'index', -1)]
        lines += [""] * (2 - len(lines)) + [" ".join(players_on_tile)]
        
        if getattr(self, "owner", None):
            houses = getattr(self, 'houses', 0)
            if isinstance(self, Utility):
                owned_utils = len([t for t in self.owner.inventory if isinstance(t, Utility)])
                rent_disp = f"{10 if owned_utils == 2 else 4}xR"
            else:
                rent_disp = f"${getattr(self, 'rent', 0)}"
            lines.append(f"{self.owner.name} [{houses}] {rent_disp}")
        else:
            price = getattr(self, "price", getattr(self, "amount", None))
            lines.append(f"${price}" if price is not None else "")
        
        color = COLORS.get(getattr(self, "group", None), "")
        return [f"{color}{line.center(11)[:11]}{'\033[0m' if color else ''}" for line in lines]

    def on_land(self, player):
        print(f"\n{player.name} landed on {self.name}.")
    
    def get_actions(self, player):
        return {}

class PurchasableTile(Tile):
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.owner = None

    def get_actions(self, player):
        actions = {}
        if self.owner is None and player.money >= self.price:
            def buy():
                player.money -= self.price
                self.owner = player
                player.inventory.append(self)
                print(f"\n{player.name} bought {self.name} for ${self.price}.")
            
            actions["b"] = (f"Buy {self.name} for ${self.price}", buy)
            
        return actions

    def on_land(self, player):
        print(f"\n{player.name} landed on {self.name}.")
        if self.owner is not None and self.owner != player:
            if isinstance(self, Utility):
                owned_utils = len([t for t in self.owner.inventory if isinstance(t, Utility)])
                multiplier = 10 if owned_utils == 2 else 4
                roll_val = getattr(player, 'last_roll', None)
                if roll_val is None:
                    roll_val = sum(game.roll())
                rent = multiplier * roll_val
            else:
                rent = self.rent
            player.money -= rent
            self.owner.money += rent
            print(f"{player.name} paid ${rent} in rent to {self.owner.name}.")

class Property(PurchasableTile):
    def __init__(self, name, group, price):
        super().__init__(name, price)
        self.group = group
        self.__rent = price // 10
        self.houses = 0

    @property
    def owns_all_color(self):
        if not getattr(self, 'owner', None):
            return False
        total = len([t for t in game.board if getattr(t, 'group', None) == self.group])
        owned = len([t for t in self.owner.inventory if getattr(t, 'group', None) == self.group])
        return total == owned

    @property
    def rent(self):
        if self.houses == 0:
            return self.__rent * 2 if self.owns_all_color else self.__rent
        return self.__rent * (3 ** self.houses)

class Railroad(PurchasableTile):
    def __init__(self, name, price=200):
        super().__init__(name, price)
        self.__rent = 25

    @property
    def rent(self):
        owned_rails = len([t for t in self.owner.inventory if isinstance(t, Railroad)])
        return self.__rent * (2 ** (owned_rails - 1)) if owned_rails > 0 else self.__rent

class Utility(PurchasableTile):
    def __init__(self, name, price=150):
        super().__init__(name, price)

class Tax(Tile):
    def __init__(self, name, amount):
        super().__init__(name)
        self.amount = amount

    def on_land(self, player):
        print(f"\n{player.name} landed on {self.name}.")
        player.money -= self.amount
        print(f"{player.name} paid ${self.amount} in taxes.")

class CardTile(Tile):
    def __init__(self, name, group=None, cards=None):
        super().__init__(name)
        self.group = group
        self.cards = cards if cards is not None else []

    def on_land(self, player):
        print(f"\n{player.name} landed on {self.name}.")
        if self.cards:
            self.apply_card(player, *random.choice(self.cards))
        else:
            print("No cards in deck!")

    def apply_card(self, player, text, action_type, value=None):
        print(f"Card Drawn: {text}")
        # I love match case statements
        match action_type:
            case "money":
                player.money += value
                print(f"{player.name} {'received' if value > 0 else 'paid'} ${abs(value)}.")
            case "move":
                player.move(value, is_absolute=True)
            case "move_relative":
                player.move(value, is_absolute=False)
            case "jail":
                player.position = 10
                player.injail = 3
                print(f"{player.name} was sent directly to Jail!")
            case "item":
                player.inventory.append(value)
                print(f"{player.name} received a {value}!")

class Jail(Tile):
    def on_land(self, player):
        print(f"\n{player.name} is Just Visiting {self.name}.")

class GoToJail(Tile):
    def on_land(self, player):
        print(f"\n{player.name} landed on {self.name}! Go directly to Jail!")
        player.position = 10
        player.injail = 3

class Go(Tile):
    def on_land(self, player):
        print(f"\n{player.name} landed on {self.name}.")
