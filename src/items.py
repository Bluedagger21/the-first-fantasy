import os
import random
import math
class Equipment():
    # Base equippable item class
    def __init__(self, name, modifiers, stack_limit=1):
        self.name = name
        self.stack_limit = stack_limit
        self.stack_size = 1
        self.modifiers = modifiers
        self.rarity = self.modifiers.setdefault("Rarity", "+0")

        if self.rarity != "+0":
            self.name += " {}".format(self.rarity)

    def getName(self):
        return self.name

    def showEverything(self):
        # Print attributes of the equipment
        print(self.name)
        print("-"*len(self.name))

        for modifier in self.modifiers:
            if modifier == "Rarity":
                continue
            else:
                if isinstance(self.modifiers[modifier], float):
                    print("{}: {:.2%}".format(modifier, self.modifiers[modifier]))
                else:
                    print("{}: {}".format(modifier, self.modifiers[modifier]))

    def getOptions(self, accessed_from="zone"):
        # Displays and prompts equipment options
        while True:
            self.showEverything()
            if accessed_from == "combat":
                print("\n*** Equipping This Item Will End Your Turn ***")
            print("\n(E)quip/Compare   (D)estroy    (Q)uit")
            choice = input("\nSelection: ").lower()
            if choice == 'e':
                return "equip"
            elif choice == 'd':
                return "destroy"
            elif choice == 'q':
                return "quit"
            # might need else continue here as well for input validation?
class Armor(Equipment):
    # Derived class from Equipment
    def __init__(self, name, slot, modifiers, stack_limit=1):
        super().__init__(name, modifiers, stack_limit)
        self.slot = slot

        if int(self.rarity) > 0:
            for modifier in self.modifiers:
                if modifier == "Physical Resist" or modifier == "Magical Resist" or modifier == "Evasion":
                    self.modifiers[modifier] *= (int(self.rarity) + 1)

class Weapon(Equipment):
    # Derived class from Equipment
    def __init__(self, name, modifiers, slot="Main Hand", stack_limit=1):
        super().__init__(name, modifiers, stack_limit)
        self.slot = slot
        self.modifiers.setdefault("Base Damage", 5)
        self.modifiers.setdefault("Random Damage", 5)
        self.modifiers.setdefault("Random Multiplier", 1)
        self.modifiers.setdefault("Crit Rate", .05)
        self.modifiers.setdefault("Crit Multiplier", 2)

        self.modifiers["Base Damage"] += int(self.rarity)

    def getCalculatedDamage(self, dealer):
        base_dmg = math.floor(dealer.total_modifiers["Base Damage"])
        rnd_dmg = math.floor(dealer.total_modifiers["Random Damage"])

        rnd_dmg_total = 0
    
        for i in range(self.modifiers["Random Multiplier"]):
            rnd_dmg_total += random.randrange(rnd_dmg) + 1
        
        return base_dmg + rnd_dmg_total

    def showEverything(self):
        # Print everything from the equipment
        print(self.name)
        print("Attack: {} + {}d({})".format(self.modifiers["Base Damage"], 
                                            self.modifiers["Random Multiplier"], 
                                            self.modifiers["Random Damage"]))
        for modifier in self.modifiers:
            if modifier == "Base Damage" or modifier == "Random Multiplier" or modifier == "Random Damage":
                continue
            else:
                print("{}: {}".format(modifier, self.modifiers[modifier]))

class Consumable():
    # Defines base members and methods for consumables
    def __init__(self, stack_limit=5, stack_size=1):
        self.stack_limit = stack_limit
        self.stack_size = stack_size
        self.slot = "consumable"

    def getName(self):
        return self.name + " (" + str(self.stack_size) + "/" + str(self.stack_limit) + ")"

    def getOptions(self, accessed_from="zone"):
        # Display and prompt options
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            self.show()
            print("\n(U)se    (D)estroy    (Q)uit")
            try:
                choice = input("\nSelection: ").lower()
            except ValueError:
                continue
            if choice == 'u':
                return "consume"
            elif choice == 'd':
                return "destroy"
            elif choice == 'q':
                return "quit"



class SmallHealthPotion(Consumable):
    def __init__(self, stack_limit=5, stack_size=1):
        super().__init__(stack_limit, stack_size)
        self.name = "Small Health Potion"
        self.effect = "Effect: Restores 20 health"
        

    def use(self, target):
        print(target.name + " used a " + self.name + ".")
        target.giveHealth(20)
        print(target.name + " gained 20 health! ({}/{})".format(
                                          target.health, 
                                          target.getMaxHealth()))
    
    def show(self):
        # Print name and effect
        print(self.getName())
        print(self.effect)

class SmallExperienceBoost(Consumable):
    def __init__(self, stack_limit=5, stack_size=1):
        super().__init__(stack_limit, stack_size)
        self.name = "Small Experience Boost"
        self.effect = "Effect: Grants 100 experience"

    def use(self, target):
        print(target.name + " used a " + self.name + ".")
        target.giveExp(100)
    
    def show(self):
        # Print name and effect
        print(self.getName())
        print(self.effect)
