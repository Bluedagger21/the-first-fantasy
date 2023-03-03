import items
import copy
import os

class Market():
    def __init__(self):
        self.inventory_list = []

    def getInventory(self, player):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("{:<2} {:<30} {:>5}".format("#", "Item", "Cost"))
            for i, item in enumerate(self.inventory_list):
                print("{:<}) {:<30} {:>5}".format(i + 1, item[0].name, item[1]))
            print("{}) Exit".format(i + 2))
            print("\nYour Gold Amount: {}".format(player.gold))
            try:
                choice = int(input("Selection: ")) - 1
            except ValueError:
                continue
            if choice <= i and choice >= 0:
                if player.takeGold(self.inventory_list[int(choice)][1]) is True:
                    player.giveItem(copy.deepcopy(self.inventory_list[int(choice)][0]))
                input("Press \"Enter\" to continue...")
            elif choice == i + 1:
                break
            else:
                continue


class BasicMarket(Market):
    def __init__(self):
        Market.__init__(self)
        self.inventory_list.extend([[items.SmallHealthPotion(), 20],
                                   [items.SmallExperienceBoost(), 25]])
