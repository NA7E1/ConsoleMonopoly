import tiles
import game

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.position = 0
        self.inventory = []
        self.injail = 0
        self.turn_active = False

    def move(self, amount, is_absolute=False):
        old_pos = self.position
        if is_absolute:
            self.position = amount % len(game.board)
        else:
            self.position = (self.position + amount) % len(game.board)

        game.build_board()

        if self.position < old_pos and amount >= 0:
            self.money += 200
            print(f"\n{self.name} passed Go and collected $200!")

        game.board[self.position].on_land(self)
    def turn(self):
        self.rolled = False
        self.turn_active = True
        
        while self.turn_active:
            actions = {}
            
            if self.injail > 0:
                game.build_board()
                print(f"{self.name} is in jail for {self.injail} more turn(s).")
                if not self.rolled:
                    if self.money >= 50:
                        actions["p"] = ("Pay $50 to get out of Jail", self.pay_out)
                    if "Get Out of Jail Free Card" in self.inventory:
                        actions["g"] = ("Use Get Out of Jail Free Card", self.use_card)
                    actions["r"] = ("Attempt to roll doubles", self.roll_for_jail)
            else:
                if not self.rolled:
                    r1, r2 = game.roll()
                    self.last_roll = r1 + r2
                    self.move(self.last_roll)
                    self.rolled = True
                
                current_tile = game.board[self.position]
                actions = current_tile.get_actions(self)

            actions["i"] = ("View inventory", self.view_inventory)
            actions["h"] = ("Build houses", self.build_houses)
            actions["e"] = ("End turn", self.end_turn)

            print("\nAvailable Actions:")
            for k, (desc, func) in actions.items():
                print(f" - {k}: {desc}")
                
            choice = input(f"\nChoose an action: ").lower()
            if choice in actions:
                actions[choice][1]()
            else:
                print("Invalid choice, please try again.")

    def pay_out(self):
        self.money -= 50
        self.injail = 0
        print(f"\n{self.name} paid $50 to get out of Jail.")

    def use_card(self):
        self.inventory.remove("Get Out of Jail Free Card")
        self.injail = 0
        print(f"\n{self.name} used a Get Out of Jail Free Card!")

    def roll_for_jail(self):
        print(f"\n{self.name} attempts to roll doubles to get out of Jail...")
        num1, num2 = game.roll()
        self.rolled = True
        self.last_roll = num1 + num2
        if num1 == num2:
            self.injail = 0
            print(f"{self.name} rolled doubles and got out of Jail!")
            self.move(self.last_roll)
        else:
            self.injail -= 1
            print(f"{self.name} failed to roll doubles and remains in Jail for {self.injail} more turn(s).")
            if self.injail == 0:
                print(f"{self.name} has served their time and is released!")

    def end_turn(self):
        if self.injail > 0 and not self.rolled:
            self.injail -= 1
            print(f"{self.name} decides to stay in jail. {self.injail} turn(s) remaining.")
            if self.injail == 0:
                print(f"{self.name} has served their time and is released!")
        self.turn_active = False

    def view_inventory(self):
        print(f"\n--- {self.name}'s Inventory ---")
        if not self.inventory:
            print("Empty.")
            return

        properties = [i for i in self.inventory if not isinstance(i, str)]
        cards = [i for i in self.inventory if isinstance(i, str)]
        
        print(f"Money: ${self.money}")
        
        if properties:
            print("\nProperties:")
            for prop in properties:
                houses_text = f" (Houses: {prop.houses})" if hasattr(prop, 'houses') else ""
                print(f" - {prop.name} [{getattr(prop, 'group', type(prop).__name__)}]{houses_text}")
        
        if cards:
            print("\nCards:")
            for card in cards:
                print(f" - {card}")
            
    def build_houses(self):
        buildable = []
        for prop in self.inventory:
            if hasattr(prop, 'owns_all_color') and prop.owns_all_color and prop.houses < 5:
                buildable.append(prop)
        
        if not buildable:
            print(f"\n{self.name} has no properties eligible for building (need all of a color group).")
            return
            
        print("\nProperties eligible for building:")
        for idx, prop in enumerate(buildable):
            print(f"{idx + 1}: {prop.name} (Houses: {prop.houses}) - Price per house: ${max(50, prop.price // 4)}")
            
        choice = input("Enter the number of the property to build on (or press Enter to cancel): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(buildable):
                prop = buildable[idx]
                house_cost = max(50, prop.price // 4)
                
                if self.money >= house_cost:
                    self.money -= house_cost
                    prop.houses += 1
                    print(f"\n{self.name} built a house on {prop.name} for ${house_cost}!")
                else:
                    print(f"\n{self.name} doesn't have enough money to build a house (costs ${house_cost}).")
