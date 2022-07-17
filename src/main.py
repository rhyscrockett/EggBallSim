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

class Pool:
    def __init__(self):
        self.pool = []

    def add(self, player):
        self.pool.append(player)

def get_position():
    """Returns a random position from a list of possible player positions."""
    pos = ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT",
            "DT", "DE", "MLB", "OLB", "CB", "SS", "FS",
            "K", "P"]
    return random.choice(pos)

def get_name():
    """Returns a random name from the names library."""
    return names.get_full_name(gender='male')

def generate_players():
    """Return a Player method that contains a pool of random generated players."""
    player_pool = Pool()
    for i in range(100):
        i = Player(get_name(), get_position(), get_price())
        player_pool.add(i)

    return player_pool

def get_price():
    """Returns a random float value rounded to the closest."""
    return round(random.uniform(660000, 50000000)

if __name__ == '__main__':
    p = Player("Rhys Crockett", "QB", "12345")

    print(p.name, p.position, p.price)
