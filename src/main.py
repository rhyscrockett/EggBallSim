# What are the components of a sport simulator?
# 1. Spreadsheet simulator ... (Good UI, Player Management, Managment Options)
# 2. Game Mechanics (Rules of Game, AI to play against each other)
# 3.

# TODO: One of the main personal requirements of this game will be to force me to use OOP paradigms
# TODO: Get fast, responsive TUI
# TODO: Random players, all of the features you can usually do in a simulator

import random # needed for random player position
import names # needed for name generation (i may do this from scratch if needed)

class Player:
    def __init__(self, name, position, price):
        self.name = name
        self.position = position
        self.price = price

    def __repr__(self):
        price = "${:,}".format(self.price)
        return f"{self.name}: ({self.position}) - {price}"

class Pool:
    def __init__(self):
        self.pool = []

    def add(self, player):
        self.pool.append(player)

class ManagerMode:
    def __init__(self, pool):
        self.pool = pool

    def print_players(self):
        """Print all players from your teams pool."""
        for i in self.pool:
            print(i)

    def print_position(self, pos):
        """Takes one argument: pos. Search for players matching the position."""
        for i in self.pool:
            if i.position == pos:
                print(i.name, i.position)

def get_position():
    """Returns a random position from a list of possible player positions."""
    pos = ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT",
            "DT", "DE", "MLB", "OLB", "CB", "SS", "FS",
            "K", "P"]
    return random.choice(pos)

def get_name():
    """Returns a random name from the names library."""
    return names.get_full_name(gender='male')

def get_price():
    """Returns a random float value rounded to the closest."""
    return round(random.uniform(660000, 50000000))

def generate_players():
    """Return a Player method that contains a pool of random generated players."""
    player_pool = Pool()
    for i in range(100):
        i = Player(get_name(), get_position(), get_price())
        player_pool.add(i)

    return player_pool

if __name__ == '__main__':
    draft = generate_players() # returns pool method
    
    manager = ManagerMode(draft.pool) # need to pass the actual pool list using the methods variable
    manager.print_players()
    manager.print_position('QB')
