import os
import loottable
import time
import random

def getAction(a, b):
    # Display combat information and prompt for action
    os.system("cls" if os.name == "nt" else "clear")
    print(b.name)
    print("Health: " + repr(b.health) + "/" + repr(b.getMaxHealth()))
    print("PWR: {:2} VIT: {:2}".format(
           b.stats["Power"],
           b.stats["Vitality"]))
    print("----------------------VERSUS")
    print(a.name)
    print("Health: " + repr(a.health) + "/" + repr(a.getMaxHealth()))
    print("PWR: {:2} VIT: {:2}".format(
           a.stats["Power"],
           a.stats["Vitality"]))
    print("\n[ACTIONS]-------------------")
    choice = input("(A)ttack    (I)nventory\n(E)nemy Info    " \
                       "(R)un Away: ").lower()
    if choice == "a" or choice == "i" or choice == "e" or choice == "r":
        return choice
    else:
        return

def combat(a, b):
    # State machine that controls combat flow between a (typically the player)
    # and b (typically player's enemy)

    c_state = None
    n_state = "standby"
    while True:
        c_state = n_state

        if c_state == "standby":
            action = getAction(a, b)
            if action == "a":
                n_state = "a_attack"
            elif action == "i":
                n_state = "inventory"
            elif action == "e":
                n_state = "info"
            elif action == "r":
                n_state = "run"
            else:
                n_state = n_state
            print("----------------------------")  # Newline

        elif c_state == "effects":
            pass

        elif c_state == "a_attack":
            if a.status_list.exists("skip"):
                print(a.name + " skipped their turn.")
                a.status_list.remove("skip")
            elif a.status_list.exists("normal"):
                proceed = a.attack(b)
                if proceed is False:
                    n_state = "standby"
                    continue
            time.sleep(1)
            if b.status_list.exists("dead"):
                n_state = "endturn"
            else:
                n_state = "b_attack"
        elif c_state == "b_attack":
            b.status_list.tick("BoT")
            if b.status_list.exists("dead"):
                print(b.name + " has been defeated!")
                n_state = "win"
            elif b.status_list.exists("skip"):
                print(b.name + " skipped their turn.")
                b.status_list.remove("skip")
                time.sleep(1)
            elif b.status_list.exists("caught"):
                time.sleep(1)
                b.attack(a)
                b.status_list.remove("caught")
            elif a.status_list.exists("normal"):
                b.attack(a)
                time.sleep(1)
            input("Press \"Enter\" to continue...")
            n_state = "endturn"

        elif c_state == "endturn":
            a.status_list.tick("EoT")
            b.status_list.tick("EoT")
            if a.status_list.exists("dead"):
                print(a.name + " has been defeated!")
                a.status_list.tick("EoC")
                a.status_list.clear()
                a.takeGold(50 * a.level)
                input("Press \"Enter\" to continue...")
                break
            elif b.status_list.exists("dead"):
                print(b.name + " has been defeated!")
                n_state = "win"
            else:
                n_state = "standby"

        elif c_state == "win":
            a.status_list.tick("EoC")
            a.status_list.clear()
            loot = b.loot_table.generateLoot()

            for x in loot:
                if isinstance(x, int):
                    a.giveGold(x)
                else:
                    if x is not None:
                        a.giveItem(x)

            a.giveXP(round((a.exp_needed / (9 + a.level)) * (b.level / a.level)))
            input("Press \"Enter\" to continue...")
            break

        elif c_state == "inventory":
            a.getInventory("combat")
            n_state = "standby"

        elif c_state == "info":
            b.getCharacterSheet()
            input("Press \"Enter\" to continue...")
            n_state = "standby"

        elif c_state == "run":
            if random.randrange(1, 4) == 1:
                print("You were able to get away!")
                a.status_list.tick("EoC")
                input("Press \"Enter\" to continue...")
                break
            else:
                print("You couldn't get away and %s caught you!" % b.name)
                n_state = "b_attack"
                b.status_list.append("caught")
