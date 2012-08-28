'''
Created on Aug 28, 2012

@author: deverett
'''
import items
import copy


class Market():
    def __init__(self):
        self.inventory_list = []

    def getInventory(self, player):
        while True:
            print "{:<2} {:<30} {:>5}".format("#", "Item", "Cost")
            for i, item in enumerate(self.inventory_list):
                print "{:<}) {:<30} {:>5}".format(i + 1, item[0].name, item[1])
            print "{}) Exit".format(i + 2)
            try:
                choice = int(raw_input("\nSelection: ")) - 1
            except ValueError:
                continue
            if choice <= i and choice >= 0:
                if player.takeGold(self.inventory_list[int(choice)][1]) \
                is True:
                    return copy.deepcopy(self.inventory_list[int(choice)][0])
                else:
                    break
            elif choice == i + 1:
                break
            else:
                continue


class BasicMarket(Market):
    def __init__(self):
        Market.__init__(self)
        self.inventory_list.extend([[items.SmallHealthPotion(), 20],
                                   [items.SmallExperienceBoost(), 25]])
