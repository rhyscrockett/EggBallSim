import random
import names
import csv
import json

class Player:
    _strength = 0
    _stamina = 0
    _speed = 0
    _agility = 0
    _accuracy = 0
    
    def __init__(self, name, position, price):
        self.name = name
        self.position = position
        self.price = price

    def __repr__(self):
        price = "${:,}".format(self.price)
        return f"{self.name}: ({self.position}) - {price}"

    def generate_position():
        """Returns a random position from a list of possible player positions."""
        pos = ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT",
               "DT", "DE", "MLB", "OLB", "CB", "SS", "FS",
               "K", "P"]
        return random.choice(pos)

    def generate_name():
        """Returns a random name from the names library."""
        return names.get_full_name(gender='male')
    
    def generate_price():
        """Returns a random float value rounded to the closes."""
        return round(random.uniform(660000, 50000000))

    def assign_attributes(self):
        pass

class Pool:
    def __init__(self):
        self.pool = []

    def add(self, player):
        self.pool.append(player)

    def print_pool(self):
        for i in self.pool:
            print(i)

def generate_players(): # technically should be a Player func (getter)
    """Returns a Player obj that contains a pool of random generated players."""
    player_pool = Pool()
    rhys = Player("Rhys Crockett", "QB", 123453) # manuall add
    player_pool.add(rhys)
    for i in range(100):
        i = Player(Player.generate_name(), Player.generate_position(), Player.generate_price())
        player_pool.add(i)

    return player_pool

class League:
    def __init__(self):
        self.league = {}
        self.nfc = {}
        self.afc = {}
        self.setup_league()

    def setup_league(self):
        with open("teams.csv", "r") as file:
            csvreader = csv.reader(file)
            next(csvreader) # remove heading
            for row in csvreader:
                if row[2] == 'NFC' and row[0] not in self.nfc:
                    self.nfc.setdefault(row[3], []).append(row[0])
                elif row[2] == 'AFC' and row[0] not in self.afc:
                    self.afc.setdefault(row[3], []).append(row[0])
        self.league.update({"NFC": self.nfc,
                            "AFC": self.afc})

    def print_league(self):
        # the easiesy/clean way to print the NFL league:
        print(json.dumps(self.league, indent=4))
        print("\n")
        # best way to run through each nested dict/list - returns the teams within divisions
        for conf, div in self.league.items():
            print("Conference:", conf) # print conf header
            for zone, team in div.items():
                print(zone, team)

    def match_division(self, t):
        '''Take a team as a parameter to find their conference and division'''
        for conf, div in self.league.items():
            for zone, team in div.items():
                if t in team:
                    return conf, zone
                else:
                    continue
        return None

    def get_stadium(self, t):
        '''Store a dictionary of team and stadium, run a search for the stadium based on home team, return stadium'''
        with open("stadiums.json") as json_file:
            stadiums = json.load(json_file)
            #print(json.dumps(data, indent=4))

        for (k,v) in stadiums.items():
            if isinstance(v.get("Team"), list): # find if the stadium is used by two
                for i in v.get("Team"): # print through each team
                    print("Stadium: " + k + " (" + str(i) + ")")
            else:
                print("Stadium: " + k + " (" + str(v.get("Team")) + ")")
                #print("Team: " + str(v.get("Team")))
                if v.get("Team") == t:
                    print("MATCH")
                    print(k)
            
class Game:
    def __init__(self, league, home_team, away_team):
        # what makes a game (time, teams, etc)
        self.home_team = home_team
        self.away_team = away_team
        self.league = league
        self.home_score = 0
        self.away_score = 0

    def setup_game(self):
        # Set the home and away teams - class for Leagues/Conferences
        self.stadium = self.league.get_stadium(self.home_team)
        # Set the date and time of the game
        self.date = datetime.datetime.now()
        self.time = datetime.time(12, 0)


if __name__ == '__main__':
    players = generate_players()
    Pool.print_pool(players)

    league = League()
    p = league.print_league()
    conf, zone = league.match_division('Green Bay Packers') # search for team and find conf
    print(conf, zone)
    s = league.get_stadium('Green Bay Packers')
    print(s)
        

    
    
