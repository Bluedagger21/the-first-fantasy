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
            expired = self.trigger(origin, target, damage)
            self.duration -= 1
            if self.duration == 0 or expired is True:
                print("The {} effect on {} expires.".format(self.name, self.owner))
                tick_packet["done"] = True
        return tick_packet
        
    def trigger(self, origin, target, damage):
        if self.callBack is None:
            return False
        else:
            self.callBack()


class Bleeding(Status):
    def __init__(self, name, owner, damage_per_turn) -> None:
        super().__init__(name, owner, duration=3, phase="BoT")
        self.damage_per_turn = damage_per_turn

    def trigger(self, origin, target, damage):
        self.owner.takeDamage(self.damage_per_turn, None)
        print("{} takes {} from the {}.".format(self.owner.name, self.damage_per_turn, self.name))

class Poison(Status):
    def __init__(self, name, owner) -> None:
        super().__init__(name, owner, duration=-1, phase="BoT")
    
    def trigger(self, phase, origin, target, damage):
        self.owner.takeDamage(self.owner.health * .1)
        print("{} takes {} damage from poison.".format(self.owner, self.damage_per_turn))
    
    def tick(self, phase, origin=None, target=None, damage=0):
        tick_packet = {"done": False}
        if phase == self.phase:
            if random.random() >= .5:
                print("The {} effect on {} expires.".format(self.name, self.owner.name))
                tick_packet["done"] = True
            else:
                self.trigger()
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
            if "damage_remaining" in tick_packet:
                damage_remaining = tick_packet["damage_remaining"]
        return damage_remaining


    def clear(self):
        for status in self.status_list:
            if (status.duration >= 0) and (status.phase == None):
                self.status_list.remove(status)
