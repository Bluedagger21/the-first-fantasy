import os
class Equipment():
    # Base equippable item class
    def __init__(self, name, stats, stack_limit = 1):
        self.name = name
        self.stack_limit = stack_limit
        self.stack_size = 1
        self.stats = stats

    def getName(self):
        return self.name

    def show(self):
        # Print attributes of the equipment
        print(self.name)
        print("Power: " + repr(self.stats[0]))
        print("Precision: " + repr(self.stats[1]))
        print("Toughness: " + repr(self.stats[2]))
        print("Vitality: " + repr(self.stats[3]))

    def getOptions(self, accessed_from="zone"):
        # Displays and prompts equipment options
        while True:
            self.show()
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

class Armor(Equipment):
    # Derived class from Equipment
    def __init__(self, name, slot, stats=[0, 0, 0, 0]):
        Equipment.__init__(self, name, stats)
        self.slot = slot

class Weapon(Equipment):
    # Derived class from Equipment
    def __init__(self, name, stats):
        Equipment.__init__(self, name, stats)
        pass

    def attack(self, dealer, receiver):
        damage = dealer.getDamage()
        print(dealer.name + " attacked for " + repr(damage) + " (-{})".format(
                                     round(damage * receiver.getArmorReduce())))
        receiver.takeDamage(damage)

class Sword(Weapon):
    def __init__(self, name, stats):
        Weapon.__init__(self, name, stats)
        self.slot = "Right Hand"
        self.options = ["Swing"]

class Mace(Weapon):
    def __init__(self, name, stats):
        Weapon.__init__(self, name, stats)
        self.slot = "Right Hand"
        self.options = ["Swing"]

class Dagger(Weapon):
    def __init__(self, name, stats):
        Weapon.__init__(self, name, stats)
        self.slot = "Right Hand"
        self.options = ["Swing"]

class Consumable():
    # Defines base members and methods for consumables
    def __init__(self, name, effect, stack_limit = 5, stack_size = 1):
        self.name = name
        self.effect = effect
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

    def show(self):
        # Print name and effect
        print(self.getName())
        print(self.effect)

class SmallHealthPotion(Consumable):
    def __init__(self):
        self.name = "Small Health Potion"
        self.effect = "Effect: Restores 20 health"
        Consumable.__init__(self, self.name, self.effect)

    def use(self, target):
        print(target.name + " used a " + self.name + ".")
        target.giveHealth(20)
        print(target.name + " gained 20 health! ({}/{})".format(
                                          target.health, 
                                          target.getMaxHealth()))

class SmallExperienceBoost(Consumable):
    def __init__(self):
        self.name = "Small Experience Boost"
        self.effect = "Effect: Grants 100 experience"
        Consumable.__init__(self, self.name, self.effect)

    def use(self, target):
        print(target.name + " used a " + self.name + ".")
        target.giveExp(100)