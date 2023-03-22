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
        print("Item Level: {}".format(self.ilvl))
        print("Quality: {}%".format(self.quality))
        print("-"*len(self.name))
        for stat in self.stats:
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
    def __init__(self, name, slot, stats, ilvl=1, rarity=0, quality=0, stack_limit=1):
        super().__init__(name, stats, ilvl, rarity, quality, stack_limit)
        self.slot = slot

        self.stats["Vitality"] = round(self.stats["Vitality"] * (1 + ((self.quality / 5) / 100)))
        self.stats["Physical Resist"] = round(self.stats["Physical Resist"] * (1 + ((self.quality / 5) / 100)))
        self.stats["Magical Resist"] = round(self.stats["Magical Resist"] * (1 + ((self.quality / 5) / 100)))
class Weapon(Equipment):
    # Derived class from Equipment
    def __init__(self, name, stats, ilvl=1, slot="Main Hand", rarity=None, quality=None, stack_limit = 1, actions=None):
        super().__init__(name, stats, ilvl, rarity, quality, stack_limit)
        self.slot = slot
        self.actions = actions
        self.stats["Power"] = round(self.stats["Power"] * (1 + ((self.quality / 5) / 100)))
        self.stats["Crit"] = round(self.stats["Power"] * (1 + ((self.quality / 5) / 100)))

    def getCalculatedDamage(self, origin, target, potency=1, damage_type="physical", crit=True):
        base_dmg = math.floor(origin.stats["Base Damage"])
        power = math.floor(origin.stats["Power"])
        total_damage = (base_dmg + power) * potency

        if crit is True:
            if random.random() <= origin.stats["Crit"] / (100 + (5 * (target.level - 1))):
                print("CRITICAL STRIKE!!!")
                total_damage *= self.stats["Crit Multiplier"]

        if damage_type == "physical":
            calc_resist = .1 * ((20 * target.level) / target.stats["Physical Resist"])
        elif damage_type == "magical":
            calc_resist = .1 * ((20 * target.level) / target.stats["Magical Resist"])
        damage_resisted = round(total_damage * calc_resist)
        total_damage = round(total_damage - damage_resisted)

        return {"Total Damage": total_damage, "Resisted Damage": damage_resisted}

    def showEverything(self):
        # Print everything from the equipment
        print(self.name)
        print("-"*len(self.name))
        print("Item Level: {}".format(self.ilvl))
        print("Quality: {}%".format(self.quality))
        print("-"*len(self.name))
        print("Actions: ")
        for action in self.actions:
            print("{}".format(action))
        print("-"*len(self.name))
        for stats in self.stats:
            print("{}: {}".format(stats, self.stats[stats]))

class Sword(Weapon):
    def __init__(self, ilvl=1, rarity=None, quality=None, stack_limit=1, name="Sword", slot="Main Hand"):
        self.stats = {"Base Damage": 5,
                      "Power": 10,
                      "Crit": 5,
                      "Crit Multiplier": 1.5}
        super().__init__(name, self.stats, ilvl, slot, rarity, quality, stack_limit)

        self.actions = ["Slash", "Parry"]

    def use(self, origin, target):
        if game.player.sword_mastery.level >= 2:
            self.actions = ["Slash (Combo)", "Parry"]

        print("\nAvailable Actions: ")
        for i, action in enumerate(self.actions):
            print("{}) {}".format(i+1, action))
        print("{}) Exit".format(i + 2))
        try:
            choice = int(input("\nSelection: ")) 
        except ValueError:
            print("Invalid choice, cancelling...")
            return False
        if choice == 1:
            self.actionSlash(origin, target)
        elif choice == 2:
            self.actionParry(origin, target)
        else:
            return False

    def actionSlash(self, origin, target):
        potency = 1.0
        damage_type = "physical"
        damage = self.getCalculatedDamage(origin, target, potency, damage_type, crit=True)
        print("You slash with your sword for {} damage!".format(damage["Total Damage"]))
        target.takeDamage(damage["Total Damage"], origin)
    
    def actionParry(self, origin, target):
        origin.status.append("parry")
        print("You prepare to counter an incoming attack.")

    def triggerParry(self, origin, target, incoming_dmg):
        origin.status.remove("parry")
        if random.random() <= 0.9:
            potency = 1.5
            damage_type = "physical"
            reduced_incoming_dmg = 0.1 * incoming_dmg
            print("You successfully parry the {}'s attack!".format(target.name))
            print("The attack is parried, you will take significantly reduced damage!".format(reduced_incoming_dmg))
            origin.takeDamage(reduced_incoming_dmg, target)
            damage = self.getCalculatedDamage(origin, target, potency, damage_type, crit=True)
            print("You counter dealing {} damage!".format(damage["Total Damage"]))
            target.takeDamage(damage["Total Damage"], origin)
        else:
            print("Your parry fails!")
            origin.takeDamage(incoming_dmg["Total Damage"], target)

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
