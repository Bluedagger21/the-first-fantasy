import os
import random
import math
import game

class Equipment():
    # Base equippable item class
    def __init__(self, name, stats, ilvl = None, rarity = None, quality = None, stack_limit = 1):
        self.name = name
        self.stack_limit = stack_limit
        self.stack_size = 1
        self.stats = stats
        
        if ilvl is None:
            self.ilvl = 1
        else:
            self.ilvl = ilvl

        if quality is None:
            self.quality = random.randint(0,100)
        else:
            self.quality = quality

        if rarity is None:
            self.rarity = 0
        else:  
            self.rarity = rarity

    def getName(self):
        return self.name

    def showEverything(self):
        # Print attributes of the equipment
        print(self.name)
        print("-"*len(self.name))

        for stat in self.stats:
            if stat == "Rarity":
                continue
            else:
                if isinstance(self.stats[stat], float):
                    print("{}: {:.2%}".format(stat, self.stats[stat]))
                else:
                    print("{}: {}".format(stat, self.stats[stat]))

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
    def __init__(self, name, slot, stats, ilvl = None, rarity = None, quality = None, stack_limit = 1):
        super().__init__(name, stats, ilvl, rarity, quality, stack_limit)
        self.slot = slot

        if int(self.rarity) > 0:
            for stat in self.stats:
                if stat == "Physical Resist" or stat == "Magical Resist" or stat == "Evasion":
                    self.stats[stat] *= (int(self.rarity) + 1)

class Weapon(Equipment):
    # Derived class from Equipment
    def __init__(self, name, stats, ilvl = None, slot="Main Hand", rarity = None, quality = None, stack_limit = 1):
        super().__init__(name, stats, ilvl, rarity, quality, stack_limit)
        self.slot = slot

    def getCalculatedDamage(self, dealer):
        base_dmg = math.floor(dealer.total_modifiers["Base Damage"])
        rnd_dmg = math.floor(dealer.total_modifiers["Random Damage"])

        rnd_dmg_total = 0
    
        for i in range(self.stats["Random Multiplier"]):
            rnd_dmg_total += random.randrange(rnd_dmg) + 1
        
        return base_dmg + rnd_dmg_total

    def showEverything(self):
        # Print everything from the equipment
        print(self.name)
        print("Attack: {} + {}d({})".format(self.stats["Base Damage"], 
                                            self.stats["Random Multiplier"], 
                                            self.stats["Random Damage"]))
        for stats in self.stats:
            if stats == "Base Damage" or stats == "Random Multiplier" or stats == "Random Damage":
                continue
            else:
                print("{}: {}".format(stats, self.stats[stats]))

class Sword(Weapon):
    def __init__(self, stats, ilvl = 1, rarity=None, quality=None, stack_limit=1, name="Sword", slot="Main Hand"):
        super().__init__(name, stats, slot, ilvl, rarity, quality, stack_limit)
        self.stats.update({"Base Damage": 10})
        self.stats.update({"Power": 10})
        self.stats.update({"Crit": 5})
        self.stats.update({"Crit Multiplier": 1.5})

        self.actions = ["Slash", "Parry"]

        if game.player.mastery.sword.level >= 2:
            self.actions = ["Slash (Combo)", "Parry"]

    def use(self, origin, target):
        print("\nAvailable Actions: ")
        for i, action in enumerate(self.actions):
            print("{}) {}".format(i, action))
        choice = input("Selection: ")
        if choice == "Slash":
            self.actionSlash(origin, target)
        if choice == "Parry":
            self.actionParry(origin, target)

    def actionSlash(self, origin, target):
        potency = 1.0
        damage = (origin.stats["Power"] + self.stats["Base Damage"]) * potency

        if random.random() <= origin.stats["Crit"] / (100 + (5 * (target.level - 1))):
            print("CRITICAL STRIKE!!!")
            damage *= self.stats["Crit Multiplier"]

        calc_resist = .1 * ((20 * target.ilvl) / target.stats["Physical Resist"])
        round(damage - (damage * calc_resist))

        target.takeDamage(damage)
    
    def actionParry(self, origin, target):
        pass
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
