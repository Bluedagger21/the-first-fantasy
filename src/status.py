import random

class Status:
    def __init__(self, name, owner, target=None, duration=-1, phase=None, callBack=None) -> None:
        self.name = name
        self.duration = duration
        self.owner = owner
        self.target = target
        self.duration = duration
        self.phase = phase
        self.callBack = callBack

    def tick(self, phase, origin, target, damage):
        tick_packet = {"done": False}
        if phase == self.phase:
            self.duration -= 1
            expired = self.trigger(origin, target, damage)
            if self.duration == 0 or expired is True:
                print("The {} effect on {} expires.".format(self.name, self.owner.name))
                input("Press \"Enter\" to continue...")
                tick_packet["done"] = True
        return tick_packet
        
    def trigger(self, origin, target, damage):
        if self.callBack is None:
            return False
        else:
            self.callBack(self)

class StatMod(Status):
    def __init__(self, name, owner, duration, stat_mod_dict: dict) -> None:
        super().__init__(name, owner, duration=duration, phase="EoT")
        self.stat_mods = stat_mod_dict

class Bleeding(Status):
    def __init__(self, name, owner, damage_per_turn) -> None:
        super().__init__(name, owner, duration=3, phase="BoT")
        self.damage_per_turn = damage_per_turn

    def trigger(self, origin, target, damage):
        self.owner.takeDamage(self.damage_per_turn, None, False)
        print("{} takes {} from the {}.".format(self.owner.name, self.damage_per_turn, self.name))

class Poison(Status):
    def __init__(self, name, owner, target) -> None:
        super().__init__(name, owner, target=target, duration=-1, phase="EoT")
    
    def trigger(self, origin, target, damage):
        self.target.takeDamage(round(self.target.health * .1), self.owner, False)
        print("{} takes {} damage from {}.".format(self.target.name, round(self.target.health * .1), self.name))
        input("Press \"Enter\" to continue...")
    
    def tick(self, phase, origin=None, target=None, damage=0):
        tick_packet = {"done": False}
        if phase == self.phase:
            if random.random() >= .5:
                print("The {} effect on {} expires.".format(self.name, self.owner.name))
                input("Press \"Enter\" to continue...")
                tick_packet["done"] = True
            else:
                self.trigger(self.owner, self.target, damage)
        return tick_packet

class Shield(Status):
    def __init__(self, name, owner, target=None, duration=1, shield_amount=0, callBack=None) -> None:
        super().__init__(name, owner, target, duration, phase="TD", callBack=callBack)
        self.shield_amount = shield_amount
        self.tick_packet = {"done": False}
    
    def tick(self, phase, origin=None, target=None, damage=0):
        if phase == self.phase and self.shield_amount > 0:
            self.trigger(origin, target, damage)
            self.duration -= 1
            if self.duration == 0 or self.shield_amount <= 0:
                print("The {} effect on {} expires.".format(self.name, self.owner.name))
                # input("Press \"Enter\" to continue...")
                # this looks like it is just causing double Enter presses for shield expire and end of combat.
                # this can be added back in if needed later
                self.tick_packet["done"] = True
            else:
                self.tick_packet["done"] = False
            return self.tick_packet
        else:
            return self.tick_packet

    def trigger(self, origin, target, incoming_damage):
        if incoming_damage <= self.shield_amount:
            absorbed_damage = incoming_damage
            print("Your {} absorbs {} damage.".format(self.name, absorbed_damage))
            self.shield_amount -= incoming_damage
            damage_left = 0
        else:
            absorbed_damage = self.shield_amount
            print("Your {} absorbs {} damage.".format(self.name, absorbed_damage))
            damage_left = incoming_damage - self.shield_amount
            self.shield_amount = 0
        self.tick_packet.update({"damage_remaining": damage_left})

class StatusList():
    def __init__(self, list=None, owner=None) -> None:
        self.owner = owner
        if list is None:
            self.status_list = []
        else:
            self.status_list = list
    
    def append(self, status):
        if isinstance(status, str):
            self.status_list.append(Status(status, self.owner))
        else:
            self.status_list.append(status)
            return True
    
    def remove(self, name):
        if isinstance(name, str):
            for status in self.status_list:
                if status.name == name:
                    self.status_list.remove(status)
                    return True
            return False
        if isinstance(name, Status):
            self.status_list.remove(name)
            return True
    
    def get(self, name) -> list:
        if isinstance(name, str):
            for status in self.status_list:
                if status.name == name:
                    return [status]
            return []
        elif isinstance(name, Status):
            status_list = []
            for status in self.status_list:
                if type(status) is type(name):
                    status_list.append(status)
            return status_list

    def exists(self, name):
        if isinstance(name, str):
            for status in self.status_list:
                if status.name == name:
                    return True
            return False
        if isinstance(name, Status):
            if name in self.status_list:
                return True
            else:
                return False
    
    def tick(self, phase, origin=None, target=None, damage=0):
        damage_remaining = damage
        for status in self.status_list:
            tick_packet = status.tick(phase, origin, target, damage_remaining)
            if tick_packet["done"] is True:
                self.remove(status)
                self.owner.updateStats()
            if "damage_remaining" in tick_packet:
                damage_remaining = tick_packet["damage_remaining"]
        return damage_remaining

    def clear(self):
        for status in self.status_list:
            if (status.duration >= 0) and (status.phase == None):
                self.status_list.remove(status)
