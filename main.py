import random
import names
import csv
import json

class Player:
    def __init__(self, name, position, price):
        self.name = name
        self.position = position
        self.price = price
        self.init_player_stats()

    def init_player_stats(self):
        # Sort positions into lists of skills
        HIGH_STRENGTH = ['RB', 'TE', 'LT', 'LG', 'C', 'RG', 'RT', 'DT', 'DE', 'MLB', 'OLB']
        HIGH_STAMINA = ['WR', 'SS', 'FS', 'CB', 'TE', 'RB']
        HIGH_SPEED = ['RB', 'WR', 'SS', 'FS', 'CB', 'OLB']
        HIGH_AGILITY = ['QB', 'RB', 'WR', 'SS', 'FS', 'CB']
        HIGH_ACCURACY = ['QB', 'WR', 'C', 'TE', 'K', 'P']
        
        # set all player stats (APPLY LARGER RANDOM NUMBER IF THEY ARE IN HIGH LIST, OTHERWISE LOW RANGE.
        self.strength = random.randint(60, 99) if self.position in HIGH_STRENGTH else random.randint(20, 60)
        self.stamina = random.randint(60, 99) if self.position in HIGH_STAMINA else random.randint(20, 60)
        self.speed = random.randint(60, 99) if self.position in HIGH_SPEED else random.randint(20, 60)
        self.agility = random.randint(60, 99) if self.position in HIGH_AGILITY else random.randint(20, 60)
        self.accuracy = random.randint(60, 99) if self.position in HIGH_ACCURACY else random.randint(20, 60)
            
    def __repr__(self):
        price = "${:,}".format(self.price)
        stats = "STR: {}\tSTA: {}\tSPD: {}\tAGL: {}\tACC: {}\n".format(self.strength, self.stamina, self.speed, self.agility, self.accuracy)
        return f"{self.name}: ({self.position}) - {price}\n{stats}"

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

class Pool:
    def __init__(self):
        self.pool = []

    def __iter__(self):
        self.i = -1
        return self
    
    def __next__(self):
        self.i += 1
        if self.i < len(self.pool):
            return self.pool[self.i]
        raise StopIteration

    def add(self, player):
        print("Adding - ", player)
        self.pool.append(player)

    def delete(self, name):
        for player in self.pool:
            if player.name == name:
                print("Removing - ", player)
                self.pool.remove(player)
            else:
                continue
        print("Player not found in pool.")

    def print_pool(self):
        for i in self.pool:
            print(i)

    def find_player(self, name):
        for player in self.pool:
            if player.name == name:
                print("Found - ", player)
                return player
            else:
                continue
        print("Player not found in pool.")

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
        #print(json.dumps(self.league, indent=4))
        #print("\n")
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
        # what makes a game (teams, score, play time etc)
        self.home_team = home_team # pass in home team
        self.away_team = away_team # pass in away team
        self.league = league # create league obj - has the get init league, get_stadium functions 
        self.home_score = 0 # variable to track home team score
        self.away_score = 0 # variable to track away team score
        self.time = 60 # variable to track 60 minute games (have to work out how I fast I want to run the game)
        self.quaters = 4 # 4 quaters to a game

    def setup_game(self):
        # Set the home and away teams - class for Leagues/Conferences
        self.stadium = self.league.get_stadium(self.home_team)
        
if __name__ == '__main__':
    def generate_players(): # technically should be a Player func (getter)
        """Returns a Player obj that contains a pool of random generated players."""
        player_pool = Pool()
        for i in range(100):
            i = Player(Player.generate_name(), Player.generate_position(), Player.generate_price())
            player_pool.add(i)
        return player_pool
    
    players = generate_players()
    Pool.print_pool(players)
    Pool.find_player(players, "Rhys Crockett") # provide Pool and Player name, finds Player and returns class.
    Pool.delete(players, "Rhys Crockett") # provide Pool and Player name, finds Player and returns class.

    # Generate (Create) new League for Game
    league = League()
    #league.print_league() # print the league (Conf: Div[N,S,E,W]

    # Match team to their conf/zone (will be used later by Game when determing who to play against)
    conf, zone = league.match_division('Green Bay Packers') # based on team, find matching conf/zone
    print(conf, zone)

    # Returns the stadium of the team passed through.
    league.get_stadium('Green Bay Packers')