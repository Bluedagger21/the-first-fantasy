import random
import market
import characters
import os
import combat
import game
import enemies

class World:
    def __init__(self) -> None:
        self.current_region = StartingRegion("Nuvrora", self)
        self.current_node = self.current_region.start
        self.last_rest_node = self.current_node

    def getCurrentNode(self):
        return self.current_node

    def travel(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            self.current_region.showMap()
            print("Current Location: {}".format(self.current_node.name))
            print("Destinations:")

            for i, node in enumerate(self.current_node.connections):
                print("{}) {}u {} - {}".format(i+1, node[1], node[2], node[0].name))
            print("{}) Cancel".format(i+2))
            try:
                choice = int(input("Selection: "))
            except ValueError:
                continue
            if not 0 < choice <= i+2:
                continue
            if choice == i+2:
                return self.current_node

            success = self.current_region.travelEncounter(self.current_node,
                                                          self.current_node.connections[choice-1][0],
                                                          self.current_node.connections[choice-1][1])
            if success is True:
                self.current_node = self.current_node.connections[choice-1][0]
                if isinstance(self.current_node, (Home, Village, Town)):
                    self.last_rest_node = self.current_node
            return self.current_node

class Region:
    def __init__(self, name, world) -> None:
        self.name = name
        self.world = world
        self.enemy_type_list = [enemies.Thief]
    def showMap(self):
        print("No map available...")

    def travelEncounter(self, start_node, destination_node, distance):
        distance_left = distance
        
        while distance_left > 0:
            os.system("cls" if os.name == "nt" else "clear")  
            type_of_encounter = self.getEncounter()
            if type_of_encounter == "combat":
                if "dead" in game.player.status:
                    print("You're too injured to fight and had to abandon your travels.")
                    input("Press \"Enter\" to continue...")
                    self.world.current_node = self.world.last_rest_node
                    return False
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

        # enemy_spawn_weights = []
        # for enemy in self.enemy_types.values():
        #     enemy_spawn_weights.append(enemy["weight"])

        spawned_enemy_type = random.choice(self.enemy_type_list)
        
        self.new_spawned_enemy = spawned_enemy_type(level)
        return self.new_spawned_enemy

class StartingRegion(Region):
    def __init__(self, name, world) -> None:
        super().__init__(name, world)

        self.node_list = []
        self.start = Home("Your House", self, 1)
        self.village1 = Village("Village of Waekefield", self, 1)
        self.wild1 = Wild("Old Stone Fields", self, 1)
        self.wild2 = Wild("Sminet Hillside", self, 2)
        self.village2 = Village("Village Laenteglos", self, 2)
        self.wild3 = Wild("Dardwell Cave", self, 3)
        self.town = Town("Town of Oar's Rest", self, 4)

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
        if "dead" in game.player.status:
                print("You're too injured to fight and had to abandon your exploration.")
                input("Press \"Enter\" to continue...")
                return False
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

    def rest(self, player):
        if "dead" in player.status:
                print("You may rest up for free! Get back out there, adventurer.")
                player.takeGold(0)
                player.giveHealth(player.getMaxHealth())
                print(player.name + " has returned to full health!")
                input("Press \"Enter\" to continue...")
        else:
            cost = player.level * 10 + 15
            while True:
                print("Cost: {}g".format(cost))
                choice = input("Accept? (Y/N): ").lower()
                if choice == 'y':
                    if player.takeGold(cost) is True:
                        player.giveHealth(player.getMaxHealth())
                        print(player.name + " has returned to full health!")
                    input("Press \"Enter\" to continue...")
                    break
                elif choice == 'n':
                    break
                else:
                    continue

class Town(Node):
    def __init__(self, name, region, level=1) -> None:
        super().__init__(name, region, level)
        self.options = ("(M)arket    (T)ravel    (R)est    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        self.market = market.BasicMarket()
    
    def rest(self, player):
        if "dead" in player.status:
                print("You may rest up for free! Get back out there, adventurer.")
                player.takeGold(0)
                player.giveHealth(player.getMaxHealth())
                print(player.name + " has returned to full health!")
                input("Press \"Enter\" to continue...")
        else:
            cost = player.level * 10 + 15
            while True:
                print("Cost: {}g".format(cost))
                choice = input("Accept? (Y/N): ").lower()
                if choice == 'y':
                    if player.takeGold(cost) is True:
                        player.giveHealth(player.getMaxHealth())
                        print(player.name + " has returned to full health!")
                    input("Press \"Enter\" to continue...")
                    break
                elif choice == 'n':
                    break
                else:
                    continue

class Home(Node):
    def __init__(self, name, region, level=1) -> None:
        super().__init__(name, region, level)
        self.options = ("(T)ravel    (R)est    (I)nventory    " +
                          "(C)haracter Sheet\n(Q)uit    (S)ave")
        
    def rest(self, player):
        print("You may rest up for free! Get back out there, adventurer.")
        player.takeGold(0)
        player.giveHealth(player.getMaxHealth())
        print(player.name + " has returned to full health!")
        input("Press \"Enter\" to continue...")
