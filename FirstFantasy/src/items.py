'''
Last changed by: Dale Everett
'''


class Equipment():
    """Defines base members and methods of equippable items"""
    def __init__(self, name, stats):
        self.name = name
        self.stats = stats

    def show(self):
        """Shows attributes of the item"""
        print self.name
        print "Power: " + repr(self.stats[0])
        print "Precision: " + repr(self.stats[1])
        print "Toughness: " + repr(self.stats[2])
        print "Vitality: " + repr(self.stats[3])

    def getOptions(self):
        """Displays and prompts equipment options"""
        while True:
            self.show()
            print "\n(E)quip    (C)ompare    (D)estroy    (Q)uit"
            choice = raw_input("\nSelection: ").lower()
            if choice == 'e':
                return "equip"
            elif choice == 'c':
                return "compare"
            elif choice == 'd':
                return "destroy"
            elif choice == 'q':
                return "quit"


class Weapon(Equipment):
    """Derived class from Equipment"""
    def __init__(self, name, stats):
        Equipment.__init__(self, name, stats)
        pass

    def attack(self, dealer, receiver):
        damage = dealer.getDamage()
        print dealer.name + " attacked for " + repr(damage) + " (-{})".format(
                                     round(damage * receiver.getArmorReduce()))
        receiver.takeDamage(damage)


class Armor(Equipment):
    """Derived class from Equipment"""
    def __init__(self, name, slot, stats=[0, 0, 0, 0]):
        Equipment.__init__(self, name, stats)
        self.slot = slot


class Consumable():
    """Defines base members and methods for consumables"""
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect
        self.slot = "consumable"

    def getOptions(self):
        """Display and prompt options"""
        while True:
            self.show()
            print "\n(U)se    (D)estroy    (Q)uit"
            choice = raw_input("\nSelection: ").lower()
            if choice == 'u':
                return "consume"
            elif choice == 'd':
                return "destroy"
            elif choice == 'q':
                return "quit"

    def show(self):
        """Print name and effect"""
        print self.name
        print self.effect


class SmallHealthPotion(Consumable):
    def __init__(self):
        self.name = "Small Health Potion"
        self.effect = "Effect: Restores 20 health"
        Consumable.__init__(self, self.name, self.effect)

    def use(self, target):
        print target.name + " used a " + self.name + "."
        target.health += 20
        if target.health > target.getMaxHealth():
            target.health = target.getMaxHealth()
        print target.name + " gained 20 health! ({}/{})".format(
                                          target.health, target.getMaxHealth())


class SmallExperienceBoost(Consumable):
    def __init__(self):
        self.name = "Small Experience Boost"
        self.effect = "Effect: Grants 100 experience"
        Consumable.__init__(self, self.name, self.effect)

    def use(self, target):
        print target.name + " used a " + self.name + "."
        target.giveExp(100)


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
