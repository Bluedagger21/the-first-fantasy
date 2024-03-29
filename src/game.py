import characters
import world
import market
import combat
import pickle
import sys
import os

player = None
worldmap = None

def titlescreen():
    # Display title and prompt whether to
    # start a new game, continue, or quit

    while True:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("The First Fantasy v0.2")
            print("Copyright (C) 2023  Dale Everett\n\n")
            print("(N)ew Game    (C)ontinue    (Q)uit")
            choice = input().lower()
            if choice == 'n' or choice == 'c' or choice == 'q':
                break
        if choice == 'n':
            newgame()
            break
        elif choice == 'c':
            tmp_bool = continuegame()
            if tmp_bool is True:
                break
        elif choice == 'q':
            os.system("cls" if os.name == "nt" else "clear")
            sys.exit()
            break


def newgame():
    # Get player name and create new world
    global worldmap
    global player
    print("\n")
    while True:
        playername = input("Enter your name: ")
        if len(playername) < 2:
            print("Name must be at least two characters long.")
        else:
            player = characters.Player(playername)
            break
    worldmap = world.Map()
    print("Prepare to begin your journey...")
    input("Press \"Enter\" to continue...")


def continuegame():
    # Prompt to choose saved game and load player and worldmap states
    global worldmap
    global player
    print("Retrieving current directory...")
    home_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    print(home_dir)
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        if os.name == "nt":  # WINDOWS
            path_separator = "\\"
        else:
            path_separator = "/"
        if not os.path.exists(home_dir + path_separator + "saves"):
            print("Creating saves directory...")
            os.makedirs(home_dir + path_separator + 'saves')
        for files in os.listdir(home_dir + path_separator + "\saves"):
            if files.endswith(".bin"):
                print(files[:-4])
        saved_file = input("\nType filename to load (C to cancel): ")
        if os.path.exists(home_dir + path_separator + "saves" +
                          path_separator + saved_file + ".bin"):
            print("Loading game...")
            f = open(home_dir + path_separator + "saves" +
                     path_separator + saved_file + '.bin', 'rb')
            player = pickle.load(f)
            worldmap = pickle.load(f)
            f.close()
            print("...Done!")
            input("Press \"Enter\" to continue...")
            return True
        elif saved_file.lower() == 'c':
            return False
        else:
            continue


def homescreen():
    # Displays current location information and prompts for actions

    # NOTE -- Need to reduce this function into something more manageable

    while True:
        current_zone = worldmap.loadZone()
        os.system("cls" if os.name == "nt" else "clear")
        choice = current_zone.getOptions()
        if choice == 'e':
            os.system("cls" if os.name == "nt" else "clear")
            if worldmap.current_zone.z_type != "town":
                explore(current_zone)
        elif choice == 'c':
            os.system("cls" if os.name == "nt" else "clear")
            player.getCharacterSheet()
            input("Press \"Enter\" to continue...")
        elif choice == 'r':
            if "dead" in player.status:
                print("You may rest up for free! Get back out there, adventurer.")
                player.takeGold(0)
                player.giveHealth(player.getMaxHealth())
                print(player.name + " has returned to full health!")
                input("Press \"Enter\" to continue...")
            else:
                cost = player.level * 10 + 15
                print("Cost: {}g".format(cost))
                if input("Accept? (Y/N): ").lower() == 'y':
                    if player.takeGold(cost) is True:
                        player.giveHealth(player.getMaxHealth())
                        print(player.name + " has returned to full health!")
                    input("Press \"Enter\" to continue...")
        elif choice == 'i':
            os.system("cls" if os.name == "nt" else "clear")
            player.getInventory()
        elif choice == 'm':
            worldmap.current_zone.market.getInventory(player)
        elif choice == 't':
            os.system("cls" if os.name == "nt" else "clear")
            worldmap.printMap()
            if worldmap.current_zone.z_type == "wild":
                explore(worldmap.current_zone)
            else:
                print("You make your way to " + worldmap.current_zone.z_name)
                input("Press \"Enter\" to continue...")
        elif choice == 'q':
            os.system("cls" if os.name == "nt" else "clear")
            sys.exit()
        elif choice == 's':
            os.system("cls" if os.name == "nt" else "clear")
            saveGame()
        else:
            continue


def saveGame():
    home_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    files = []
    if os.name == "nt":  # WINDOWS
        path_separator = "\\"
    else:
        path_separator = "/"
    if not os.path.exists(home_dir + path_separator + 'saves'):
        os.makedirs(home_dir + path_separator + 'saves')
        print(home_dir)
    print("Existing saves: ")
    for file in os.listdir(home_dir + path_separator + "\saves"):
        if file.endswith(".bin"):
            print(file[:-4])
            files.append(file[:-4])
    save_name = input("\nSave game as: ")
    if save_name in files:
        choice = input("Save files already exist for this name. Overwrite? (Y/N) ").lower()
        if choice == "n":
            print("Saving cancelled.")
            input("Press \"Enter\" to continue...")
            return
    f = open(home_dir + path_separator + 'saves' + path_separator \
        + save_name + '.bin', 'wb')
    print("Saving game...")
    pickle.dump(player, f, protocol=0)
    pickle.dump(worldmap, f, protocol=0)
    f.close()
    print("...Done!")
    input("Press \"Enter\" to continue...")

def explore(current_zone):
    # Decides if an encounter occurs or not
    os.system("cls" if os.name == "nt" else "clear")
    if "dead" in player.status:
        print("You're too injured to fight. Rest at a town!")
        input("Press \"Enter\" to continue...")
        return
    action = current_zone.getAction()
    if action == "encounter":
        opponent = current_zone.getEnemy()
        combat.combat(player, opponent)
    elif action == "nothing":
        print("Nothing of interest was found...")
        input("Press \"Enter\" to continue...")
