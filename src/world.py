import zone
import random
import market
import characters
import os
import combat
import game

class World:
    def __init__(self) -> None:
        self.current_region = StartingRegion("Nuvrora", self)
        self.current_node = self.current_region.start

    def loadZone(self):
        return self.current_node

    def travel(self):
        while True:
            self.current_region.showMap()
            print("Current Location: {}".format(self.current_node.name))
            print("Destinations:")

            for i, node in enumerate(self.current_node.connections):
                print("{}) {}u {} - {}".format(i+1, node[1], node[2], node[0].name))
            choice = int(input("Selection: "))
            if 0 > choice <= i+1:
                continue

            success = self.current_region.travelEncounter(self.current_node,
                                                          self.current_node.connections[choice-1][0],
                                                          self.current_node.connections[choice-1][1])
            if success is True:
                self.current_node = self.current_node.connections[choice-1][0]
            return self.current_node

class Region:
    def __init__(self, name, world) -> None:
        self.name = name
        self.world = world
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

    def travelEncounter(self, start_node, destination_node, distance):
        distance_left = distance
        
        while distance_left > 0:
            os.system("cls" if os.name == "nt" else "clear")
            if "dead" in game.player.status:
                print("You're too injured to fight and had to abandon your travels.")
                input("Press \"Enter\" to continue...")
                return False
            type_of_encounter = self.getEncounter()
            if type_of_encounter == "combat":
                self.startCombat(destination_node.level)
            distance_left -= 1
            if distance_left > 0:
                os.system("cls" if os.name == "nt" else "clear")
                print("You take a short rest before continuing your travels.")
                input("Press \"Enter\" to continue...")
        return True

    def getEncounter(self):
        return False

    def startCombat(self, level):
        opponent = self.getEnemy(level)
        combat.combat(game.player, opponent)

    def getEnemy(self, level):
        # Create an enemy and return it
        minimum = round(level * .75)
        maximum = round(level * 1.25)
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

class StartingRegion(Region):
    def __init__(self, name, world) -> None:
        super().__init__(name, world)

        self.node_list = []
        self.start = Home("Your House", self, 1)
        self.village1 = Village("Waekefield", self, 1)
        self.wild1 = Wild("Old Stone Fields", self, 1)
        self.wild2 = Wild("Sminet Hillside", self, 1)
        self.village2 = Village("Laenteglos", self, 1)
        self.wild3 = Wild("The Scarlet Pinnacle", self, 1)
        self.wild4 = Wild("Dardwell Cave", self, 1)
        self.town = Town("Oar's Rest", self, 1)

        self.start.addConnection([(self.village1, 1, "East")])
        self.village1.addConnection([(self.start, 1, "West"), (self.wild1, 1, "South")])
        self.wild1.addConnection([(self.village1, 1, "North"), (self.village2, 1, "East")])
        self.village2.addConnection([(self.wild1, 1, "West"), (self.wild2, 2, "North"), (self.wild3, 3, "East"), (self.town, 3, "South")])
        self.wild2.addConnection([(self.village2, 2, "South")])
        self.wild3.addConnection([(self.village2, 3, "West")])
        self.town.addConnection([(self.village2, 3, "North")])

        self.encounters = [("combat", 20), ("nothing", 4)]

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

    def getEncounter(self):
        option_weights = []
        options = []
        for e, w in self.encounters:
            option_weights.append(w)
            options.append(e)
        return random.choices(options, weights=option_weights)[0]

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
    
    def getEncounter(self):
        return False

class Wild(Node):
    def __init__(self, name, region, level=1) -> None:
        super().__init__(name, region, level)
        self.options = ("(E)xplore    (T)ravel    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        self.encounters = [("combat", 20), ("nothing", 4)]

    def getEncounter(self):
        option_weights = []
        options = []
        for e, w in self.encounters:
            option_weights.append(w)
            options.append(e)
        return random.choices(options, weights=option_weights)[0]
    
    def explore(self):
        type_of_encounter = self.getEncounter()
        if type_of_encounter == "combat":
                self.region.startCombat(self.level)
        else:
            print("You found nothing of interest.")
            input("Press \"Enter\" to continue...")
    
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
