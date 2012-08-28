'''
Last changed by: Ryan Breaker
'''
import characters
import world
import combat
import cPickle
import sys
import os

player = None
worldmap = None


def titlescreen():
    """
    Display title and prompt whether to
    start a new game, continue, or quit
    """
    choice = ''
    while True:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print "The First Fantasy v0.1"
            print "Copyright (C) 2012  Dale Everett\n\n"
            print "(N)ew Game    (C)ontinue    (Q)uit"
            choice = raw_input().lower()
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
    """Get player name and create new world"""
    global worldmap
    global player
    print "\n"
    while True:
        playername = raw_input("Enter your name: ")
        if len(playername) < 2:
            print "Name must be at least two characters long."
        else:
            player = characters.Player(playername)
            break
    worldmap = world.Map()
    print "Prepare to begin your journey..."
    raw_input("Press \"Enter\" to continue...")


def continuegame():
    """Prompt to choose saved game and load player and worldmap states"""
    global worldmap
    global player
    print "Retrieving current directory..."
    home_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    print home_dir
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        if os.name == "nt":  # WINDOWS
            path_separator = "\\"
        else:
            path_separator = "/"
        if not os.path.exists(home_dir + path_separator + "saves"):
            print "Creating saves directory..."
            os.makedirs(home_dir + path_separator + 'saves')
        for files in os.listdir(home_dir + path_separator + "\saves"):
            if files.endswith(".bin"):
                print files[:-4]
        saved_file = raw_input("\nType filename to load (C to cancel): ")
        if os.path.exists(home_dir + path_separator + "saves" +
                          path_separator + saved_file + ".bin"):
            print "Loading game..."
            f = open(home_dir + path_separator + "saves" +
                     path_separator + saved_file + '.bin', 'rb')
            player = cPickle.load(f)
            worldmap = cPickle.load(f)
            f.close()
            print "...Done!"
            raw_input("Press \"Enter\" to continue...")
            return True
        elif saved_file.lower() == 'c':
            return False
        else:
            continue


def homescreen():
    """Displays current location information and prompts for actions

    NOTE -- Need to reduce this function into something more manageable"""
    choice = ''
    while True:
        current_zone = worldmap.loadZone()
        os.system("cls" if os.name == "nt" else "clear")
        choice = current_zone.getOptions()
        if choice == 'e':
            os.system("cls" if os.name == "nt" else "clear")
            explore(current_zone)
        elif choice == 'c':
            os.system("cls" if os.name == "nt" else "clear")
            player.getCharacterSheet()
            raw_input("Press \"Enter\" to continue...")
        elif choice == 'r':
            cost = player.level * 10 + 15
            print "Cost: {}g".format(cost)
            if raw_input("Accept? (Y/N): ").lower() == 'y':
                if player.gold >= cost:
                    player.gold -= cost
                    player.giveHealth(player.getMaxHealth())
                    print player.name + " has returned to full health!"
                else:
                    print "You don't have enough gold!"
                raw_input("Press \"Enter\" to continue...")
        elif choice == 'i':
            os.system("cls" if os.name == "nt" else "clear")
            player.getInventory()
        elif choice == 't':
            os.system("cls" if os.name == "nt" else "clear")
            worldmap.printMap()
            print "You make your way to " + worldmap.current_zone.z_name
            if worldmap.current_zone.z_type == "wild":
                explore(worldmap.current_zone)
            else:
                raw_input("Press \"Enter\" to continue...")
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
    if os.name == "nt":  # WINDOWS
        path_separator = "\\"
    else:
        path_separator = "/"
    if not os.path.exists(home_dir + path_separator + 'saves'):
        os.makedirs(home_dir + path_separator + 'saves')
        print home_dir
    print "Existing saves: "
    for files in os.listdir(home_dir + path_separator + "\saves"):
            if files.endswith(".bin"):
                print files[:-4]
    save_name = raw_input("\nSave game as: ")
    f = open(home_dir + path_separator + 'saves' + path_separator \
             + save_name + '.bin', 'wb')
    print "Saving game..."

    cPickle.dump(player, f, protocol=0)
    cPickle.dump(worldmap, f, protocol=0)
    f.close()
    print "...Done!"
    raw_input("Press \"Enter\" to continue...")


def explore(current_zone):
    """Decides if an encounter occurs or not"""
    os.system("cls" if os.name == "nt" else "clear")
    action = current_zone.getAction()
    if action == "encounter":
        opponent = current_zone.getEnemy()
        combat.combat(player, opponent)
    elif action == "nothing":
        print "Nothing of interest was found..."
        raw_input("Press \"Enter\" to continue...")
