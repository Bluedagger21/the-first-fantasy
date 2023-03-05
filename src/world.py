import zone
import random
import os
import pprint

class Map:
    def __init__(self):
        # Define zone names and sets of enemies to use in zones
        self.wild_names = ["Dark Forest", "Evil Bridge", "Desolate Plains",
                           "Old Ruins", "Torched Grassland", "Black Swamp",
                           "Endless Wastes", "Sunless Canyon", "Foul Bog",
                           "Terror Isle"]
        self.town_names = ["Your House", "Cheery Inn", "Joe's Bed & Breakfast"]
        self.enemy_types = {"Thief": {"weight" : 10, 
                                       "attribute_weights" : [2,5,3]},
                            "Goblin": {"weight" : 5, 
                                       "attribute_weights" : [3,4,3]},
                            "Spider": {"weight" : 5, 
                                       "attribute_weights" : [3,5,2]},
                            "Kobold": {"weight" : 5,
                                       "attribute_weights" : [5,3,2]}}

        random.shuffle(self.wild_names)
        random.shuffle(self.town_names)

        starting_zone = self.town_names.pop(
                        self.town_names.index("Your House"))
        self.current_zone = zone.Town(starting_zone, 0)
        self.placeZone(self.current_zone, 1)

    def placeZone(self, cur, dr, root=None):
        # Recursively place zones outwards from 'Your House'
        if root is None:
            home_flag = 1
        else:
            home_flag = 0
        if (len(self.wild_names) > 0 or len(self.town_names) > 0 or
                                        len(cur.neighbors) != 0):
            neighbors_to_place = random.randint(max(0, home_flag),
                                                min(3 + home_flag,
                                                    len(self.wild_names)))
            neighbor_list = []

            if (cur.z_type != "town" and neighbors_to_place > 0 and
                len(self.town_names) > 0):
                if random.randint(0, 10) > 8:
                    created_town = zone.Town(self.town_names.pop(), dr, cur)
                    neighbor_list.append(created_town)
                    neighbors_to_place -= 1
            while neighbors_to_place > 0:
                created_wild = zone.Wild(self.wild_names.pop(), dr,
                                         self.enemy_types, cur)
                neighbor_list.append(created_wild)
                neighbors_to_place -= 1
            while len(neighbor_list) > 0:
                cur.neighbors.append(neighbor_list.pop())

            for i, n in enumerate(cur.neighbors):
                if n != root:
                    dr += 1
                    self.placeZone(cur.neighbors[i], dr, cur)

    def printMap(self):
        # Uses pprint to print zone list in map_layer
        map_layer = []
        j_map = 0
        for i in range(len(self.current_zone.neighbors)):
            map_layer.append(self.current_zone.neighbors[i].z_name)
            if len(self.current_zone.neighbors[i].neighbors) > 1:
                map_layer.append([])
                j_map += 1
                self.generateMapLayer(self.current_zone.neighbors[i],
                                      self.current_zone, map_layer[j_map])
            j_map += 1

        pp = pprint.PrettyPrinter(indent=4)
        possibilities = len(self.current_zone.neighbors)
        i = 0
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            pp.pprint(map_layer)
            for i in range(possibilities):
                print(repr(i + 1) + ") " +
                       self.current_zone.neighbors[i].z_name)
            print(repr(i + 2) + ") Cancel")
            try:
                choice = int(input("\nSelection: "))
            except ValueError:
                continue
            if choice < i + 2 and choice > 0:
                self.current_zone = self.current_zone.neighbors[choice - 1]
                break
            elif choice == i + 2:
                break
            else:
                continue

    def generateMapLayer(self, cur_zone, root_zone, map_layer):
        # Recursively places neighboring zones in current layer
        j_map = 0
        for i in range(len(cur_zone.neighbors)):
            if cur_zone.neighbors[i].z_name != root_zone.z_name:
                map_layer.append(cur_zone.neighbors[i].z_name)
                if len(cur_zone.neighbors[i].neighbors) > 1:
                    map_layer.append([])
                    j_map += 1
                    self.generateMapLayer(cur_zone.neighbors[i],
                                          cur_zone,
                                          map_layer[j_map])
                j_map += 1

    def loadZone(self):
        return self.current_zone
