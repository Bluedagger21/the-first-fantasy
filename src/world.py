import zone
import random
import market
import characters
import os
import pprint

class World:
    def __init__(self) -> None:
        self.current_region = StartingRegion("Nuvrora")
        self.current_node = self.current_region.start

    def loadZone(self):
        return self.current_node

    def travel(self):
        while True:
            self.current_region.showMap()
            print("Current Location: {}".format(self.current_node.name))
            print("Destinations:")

            for i, node in enumerate(self.current_node.connections):
                print("{}) {}u - {}".format(i+1, node[1], node[0].name))
            choice = int(input("Selection: "))
            if 0 > choice >= i:
                continue

            self.current_node = self.current_node.connections[choice-1][0]
            return self.current_node

class Region:
    def __init__(self, name) -> None:
        self.name = name
        self.enemy_types = {"Thief": {"weight": 10,
                                      "attribute_weights": [2, 5, 3],
                                      "weapon": {"Base Damage": 5,
                                                 "Random Damage": 5,
                                                 "Random Multiplier": 1,
                                                 "Base Crit Rate": .1,
                                                 "Crit Multiplier": 2}},
                            "Goblin": {"weight": 5,
                                       "attribute_weights": [3, 4, 3],
                                       "weapon": {"Base Damage": 3,
                                                  "Random Damage": 3,
                                                  "Random Multiplier": 2,
                                                  "Base Crit Rate": .05,
                                                  "Crit Multiplier": 2}},
                            "Spider": {"weight": 5,
                                       "attribute_weights": [3, 5, 2],
                                       "weapon": {"Base Damage": 0,
                                                  "Random Damage": 10,
                                                  "Random Multiplier": 1,
                                                  "Base Crit Rate": .05,
                                                  "Crit Multiplier": 3}},
                            "Kobold": {"weight": 5,
                                       "attribute_weights": [5, 3, 2],
                                       "weapon": {"Base Damage": 8,
                                                  "Random Damage": 2,
                                                  "Random Multiplier": 1,
                                                  "Base Crit Rate": .05,
                                                  "Crit Multiplier": 2}}}
    def showMap(self):
        print("No map available...")
class StartingRegion(Region):
    def __init__(self, name) -> None:
        super().__init__(name)

        self.node_list = []
        self.start = Home("Your House", self, 1)
        self.village1 = Village("Waekefield", self, 1)
        self.wild1 = Wild("Old Stone Fields", self, 1)
        self.wild2 = Node("Sminet Hillside", self, 1)
        self.village2 = Village("Laenteglos", self, 1)
        self.wild3 = Wild("The Scarlet Pinnacle", self, 1)
        self.wild4 = Wild("Dardwell Cave", self, 1)
        self.town = Town("Oar's Rest", self, 1)

        self.start.addConnection([(self.village1, 1)])
        self.village1.addConnection([(self.start, 1), (self.wild1, 1)])
        self.wild1.addConnection([(self.village1, 1), (self.village2, 1)])
        self.village2.addConnection([(self.wild1, 1), (self.wild2, 2), (self.wild3, 3), (self.town, 3)])
        self.wild2.addConnection([(self.village2, 2)])
        self.wild3.addConnection([(self.village2, 3)])
        self.town.addConnection([(self.village2, 3)])

    def showMap(self):
        print("╔════════════════════╗")
        print("║▲▲.......[W].......▲║")
        print("║▲[H]━[V]..┃........▲║")
        print("║......┃...┃......▲▲▲║")
        print("║.....[W]━[V]━━━[W]▲▲║")
        print("║..........┃......▲▲▲║")
        print("║..........┃.......▲▲║")
        print("║..........┃........▲║")
        print("║.....▒▒▒.[T]........║")
        print("║....▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒║")
        print("╚════════════════════╝")

    

class Node:
    def __init__(self, name, region, level=1) -> None:
        self.name = name
        self.region = region
        self.level = level
        self.connections = []
    
    def addConnection(self, nodes):
        self.connections = nodes
        self.connections.sort(key=lambda a: a[1])
    
    def getOptions(self):
        # Print options and prompt for choice
        print("You are currently at: ", self.name)
        print("What would you like to do?\n", self.options)
        return input().lower()

class Wild(Node):
    def __init__(self, name, region, level=1) -> None:
        super().__init__(name, region, level)
        self.options = ("(E)xplore    (T)ravel    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        self.actions = [("encounter", 20), ("nothing", 4)]
        self.enemy_types = self.region.enemy_types
        self.encounters = [("encounter", 20), ("nothing", 4)]

    def getEnemy(self):
        # Create an enemy and return it
        minimum = round(self.level * .75)
        maximum = round(self.level * 1.25)
        random_value = random.randint(minimum, maximum)

        enemy_spawn_weights = []
        for enemy in self.enemy_types.values():
            enemy_spawn_weights.append(enemy["weight"])

        enemy_name_list = list(self.enemy_types.keys())

        spawned_enemy_name = random.choices(enemy_name_list, weights=enemy_spawn_weights)[0]
        
        self.new_spawned_enemy = characters.Enemy(spawned_enemy_name, 
                                                random_value,
                                                self.enemy_types[spawned_enemy_name]["attribute_weights"],
                                                self.enemy_types[spawned_enemy_name]["weapon"])
        return self.new_spawned_enemy

    def getEncounter(self):
        option_weights = []
        options = []
        for e, w in self.encounters:
            option_weights.append(w)
            options.append(e)
        return random.choices(options, weights=option_weights)[0]
class Village(Node):
    def __init__(self, name, region, level=1) -> None:
        super().__init__(name, region, level)
        self.options = ("(M)arket    (T)ravel    (R)est    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        self.market = market.BasicMarket()

class Town(Node):
    def __init__(self, name, region, level=1) -> None:
        super().__init__(name, region, level)
        self.options = ("(M)arket    (T)ravel    (R)est    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        self.market = market.BasicMarket()

class Home(Node):
    def __init__(self, name, region, level=1) -> None:
        super().__init__(name, region, level)
        self.options = ("(T)ravel    (R)est    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        

    # def printMap(self):
    #     # Uses pprint to print zone list in map_layer
    #     map_layer = []
    #     j_map = 0
    #     for i in range(len(self.current_zone.neighbors)):
    #         map_layer.append(self.current_zone.neighbors[i].z_name)
    #         if len(self.current_zone.neighbors[i].neighbors) > 1:
    #             map_layer.append([])
    #             j_map += 1
    #             self.generateMapLayer(self.current_zone.neighbors[i],
    #                                   self.current_zone, map_layer[j_map])
    #         j_map += 1

    #     pp = pprint.PrettyPrinter(indent=4)
    #     possibilities = len(self.current_zone.neighbors)
    #     i = 0
    #     while True:
    #         os.system("cls" if os.name == "nt" else "clear")
    #         pp.pprint(map_layer)
    #         for i in range(possibilities):
    #             print(repr(i + 1) + ") " +
    #                    self.current_zone.neighbors[i].z_name)
    #         print(repr(i + 2) + ") Cancel")
    #         try:
    #             choice = int(input("\nSelection: "))
    #         except ValueError:
    #             continue
    #         if choice < i + 2 and choice > 0:
    #             self.current_zone = self.current_zone.neighbors[choice - 1]
    #             break
    #         elif choice == i + 2:
    #             break
    #         else:
    #             continue

    # def generateMapLayer(self, cur_zone, root_zone, map_layer):
    #     # Recursively places neighboring zones in current layer
    #     j_map = 0
    #     for i in range(len(cur_zone.neighbors)):
    #         if cur_zone.neighbors[i].z_name != root_zone.z_name:
    #             map_layer.append(cur_zone.neighbors[i].z_name)
    #             if len(cur_zone.neighbors[i].neighbors) > 1:
    #                 map_layer.append([])
    #                 j_map += 1
    #                 self.generateMapLayer(cur_zone.neighbors[i],
    #                                       cur_zone,
    #                                       map_layer[j_map])
    #             j_map += 1

    # def loadZone(self):
    #     return self.current_zone
