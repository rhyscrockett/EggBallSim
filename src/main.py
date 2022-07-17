# What are the components of a sport simulator?
# 1. Spreadsheet simulator ... (Good UI, Player Management, Managment Options)
# 2. Game Mechanics (Rules of Game, AI to play against each other)
# 3.

# TODO: One of the main personal requirements of this game will be to force me to use OOP paradigms
# TODO: Get fast, responsive TUI
# TODO: Random players, all of the features you can usually do in a simulator

import random # needed for random player position

class Player:
    def __init__(self, name, position, price):
        self.name = name
        self.position = position
        self.price = price

def get_position():
    pos = ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT",
            "DT", "DE", "MLB", "OLB", "CB", "SS", "FS",
            "K", "P"]
    return random.choice(pos)

if __name__ == '__main__':
    p = Player("Rhys Crockett", "QB", "12345")

    print(p.name, p.position, p.price)
