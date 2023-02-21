'''
Last changed by: Dale Everett
'''
import characters
import market
from weightedchoice import weighted_choice_sub
import random


class Zone:
    """Defines members and methods of each location in the world"""

    def __init__(self, name, dr, first_neighbor):
        self.z_name = name
        self.z_dr = dr
        self.neighbors = []
        if first_neighbor is not None:
            self.neighbors.append(first_neighbor)

    def printZone(self, root):
        """Print neighbors around this zone"""
        for z in self.neighbors:
            if z.z_name != root.z_name:
                print (z.z_name)


class Wild(Zone):
    """"Wild zones are hostile and contain enemies"""

    def __init__(self, name, dr, enemy_list, first_neighbor=None):
        Zone.__init__(self, name, dr, first_neighbor)

        self.z_type = "wild"
        self.z_options = ("(E)xplore    (T)ravel    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        self.z_actions = [("encounter", 20), ("nothing", 4)]
        self.z_enemy_list = enemy_list

    def getEnemy(self):
        """Create an enemy and return it"""
        minimum = round(self.z_dr * .75)
        maximum = round(self.z_dr * 1.25)
        random_value = random.randint(minimum, maximum)
        stats = self.z_enemy_list[weighted_choice_sub(
                                 [x[1] for x in self.z_enemy_list])]
        return characters.Enemy(stats[0], stats[2], random_value)

    def getAction(self):
        """Decide if an encounter happens or not"""
        return self.z_actions[weighted_choice_sub(
                             [x[1] for x in self.z_actions])][0]

    def getOptions(self):
        """Print options and prompt for choice"""
        print ("You are currently at: ", self.z_name)
        print ("What would you like to do?\n", self.z_options)
        return input().lower()


class Town(Zone):
    """Town zones pose no threat and offer shops and rest"""
    def __init__(self, name, dr, first_neighbor=None):
        Zone.__init__(self, name, dr, first_neighbor)
        self.z_type = "town"
        self.z_options = ("(M)arket    (T)ravel    (R)est    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        self.market = market.BasicMarket()
        """
        Prototype for future market creation
        if dr in range(2):
            self.market = market.BasicMarket()
        """

    def getOptions(self):
        """Print options and prompt for choice"""
        print ("You are currently at: ", self.z_name)
        print ("What would you like to do?\n", self.z_options)
        return input().lower()
