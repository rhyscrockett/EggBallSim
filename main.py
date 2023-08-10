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
        self.schedule = []

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
        
    def generate_schedule(self): # (NOT INCLUDING BYE, OR PARITY GAMES) 224/272
        conference_matchups = [] # conference games (NFC, AFC)
        division_matchups = [] # division games (NFC West, NFC North)
        interconference_matchups = [] # division games from other conf (NFC East, AFC South)
        parity_matchups = [] # games against similar ranked teams in each of the two itraconference div

        # 1. Six games against divisonal opponents (returns 96 games)
        for division in self.nfc.values():
            division_matchups.extend(self._generate_divisional_matchups(division))
        for division in self.afc.values():
            division_matchups.extend(self._generate_divisional_matchups(division))

        # 2. Four games against teams from a division within its conference (returns 64 games)
        conference_matchups.extend(self._generate_conference_matchups())

        # 3. Four games against teams from a division in the other conference (returns 64 games)
        interconference_matchups.extend(self._generate_interconference_matchups())

        # 4. Two games against teams from the same divisional rank in each of the two intraconference divisions (should return 32 games - WIP)
        remaining_division_matchups = self._get_remaining_divisions(conference_matchups, self.nfc)
        parity_matchups.extend(self._generate_parity_matchups(remaining_division_matchups))


        # 5. The 17th game is an additional game against a non-conference opponent from a division that the team is not scheduled to play. Matchups are based on division ranking from the previous season. (should return 16 games - WIP)


        schedule = conference_matchups + division_matchups + interconference_matchups #+ parity_matchups

        # shuffle schedule
        random.shuffle(schedule)

        # assign by weeks randomly to each team
        #bye_weeks = self._assign_bye_weeks(self.league.keys(), start_week=4, end_week=12)

        # Create the final schedule with bye weeks
        #final_schedule = []
        #for week in range(1, 19): # 18 weeks
        #    if week not in bye_weeks:
        #        final_schedule.extend(self._filter_schedule(schedule, week))
        #    else:
        #        teams_on_bye = bye_weeks[week]
        #        for team in teams_on_bye:
        #            final_schedule.append((team, "BYE"))

        #self.schedule = final_schedule

        return schedule
    
    def _filter_schedule(self, schedule, week):
        return [(home_team, away_team) for home_team, away_team in schedule if home_team != "BYE" and away_team != "BYE"]
    
    def _assign_bye_weeks(self, teams, start_week, end_week):
        # DO NOT UNDERSTAND THE FORMAT FOR BYE WEEKS IN NFL - THEREFORE, WILL USE THE FORMAT 4 TEAMS ON BYE FOR 8 WEEKS (STARS WEEK 4, ENDS WEEK 12)
        bye_weeks = {}
        bye_week_slots = list(range(start_week, end_week + 1))
        for team in teams:
            bye_week = random.choice(bye_week_slots)
            bye_week_slots.remove(bye_week)
            bye_weeks.setdefault(bye_week, []).append(team)

    def _get_remaining_divisions(self, division_matchups, conference_teams):
        paired_divisions = set()

        for home_team, away_team in division_matchups:
            home_team_division = None
            away_team_division = None

            for division, teams in conference_teams.items():
                if home_team in teams:
                    home_team_division = division
                if away_team in teams:
                    away_team_division = division

            if home_team_division and away_team_division:
                paired_divisions.add(tuple(sorted((home_team_division, away_team_division)))) # remove tuple and sorted to get both ways (i.e. home, away/away, home)

        remaining_divisions = list(conference_teams.keys())
        parity_division_pairs = []

        for division1 in remaining_divisions:
            for division2 in paired_divisions:
                if division1 != division2[0] and division1 != division2[1]:
                    parity_division_pairs.append((division1, division2[0]))
                    parity_division_pairs.append((division1, division2[1]))

        print("Paired Divisions:")
        for division_pair in paired_divisions:
            print(f"{division_pair}\n")

        return parity_division_pairs

    def _generate_conference_matchups(self):
        matchups = []
        for conference_division in [self.nfc, self.afc]:
            divisions = list(conference_division.values())
            random.shuffle(divisions)

            for division1, division2 in zip(divisions[0::2], divisions[1::2]):
                division1_teams = [team for team in division1]
                division2_teams = [team for team in division2]

                for division1_team in division1_teams:
                    opponents = list(division2_teams) # make a copy of teams to work with

                    # randomly select 2 home and 2 away opponents from the AFC division
                    home_games = random.sample(opponents, 2)
                    opponents = [team for team in opponents if team not in home_games] # remove the selected home opponents
                    away_games = random.sample(opponents, 2)

                    for division2_team in home_games:
                        matchups.append((division1_team, division2_team))
                    for division2_team in away_games:
                        matchups.append((division2_team, division1_team))
                
        return matchups
    
    def _generate_divisional_matchups(self, division_teams):
        matchups = []
        for i in range(len(division_teams)):
            home_team = division_teams[i]
            for j in range(i + 1, len(division_teams)):
                away_team = division_teams[j]
                matchups.append((home_team, away_team)) # add both home_team, away_team
                matchups.append((away_team, home_team)) # away_team, home_team to ensure all teams play home and away
        random.shuffle(matchups) 
        return matchups

    def _generate_interconference_matchups(self):
        matchups = []
        nfc_divisions = list(self.nfc.values())
        afc_divisions = list(self.afc.values())

        random.shuffle(afc_divisions) # shuffle the AFC Divisions to ensure uniqueness

        for nfc_divisions, afc_divisions in zip(nfc_divisions, afc_divisions):
            afc_teams = [team for team in afc_divisions] # get all AFC teams in the division
            for nfc_team in nfc_divisions:
                afc_opponents = list(afc_teams) # make a copy of AFC teams to work with

                # randomly select 2 home and 2 away opponents from the AFC division
                home_opponents = random.sample(afc_opponents, 2)
                afc_opponents = [team for team in afc_opponents if team not in home_opponents] # remove the selected home opponents
                away_opponents = random.sample(afc_opponents, 2)

                for afc_team in home_opponents:
                    matchups.append((nfc_team, afc_team))
                for afc_team in away_opponents:
                    matchups.append((afc_team, nfc_team))
        return matchups


    def _generate_parity_matchups(self, parity_division_pairs):
        matchups = []
        
        #print(parity_division_pairs)
        for division_pair in parity_division_pairs:
            print(division_pair)
            division1, division2 = division_pair

            division1_teams = self.nfc[division1]
            division2_teams = self.nfc[division2]

            for rank in range(len(division1_teams)):
                team1 = division1_teams[rank]
                team2 = division2_teams[rank]

                matchups.append((team1, team2))
                matchups.append((team2, team1))
            
        print(len(matchups))

        return matchups
    
    def print_schedule(self, schedule):
        # Printing the schedule in a clean formatted table
        print("Week\tAway Team\t@\tHome Team")
        for week, (away_team, home_team) in enumerate(schedule, start=1):
            print(f"{week}\t{away_team} \t@\t{home_team} ")

    def print_team_schedule(self, team_name, schedule):
        print(f"Schedule for {team_name}:")
        team_schedule = [(week, away_team, home_team) for week, (away_team, home_team) in enumerate(schedule, start=1) if team_name in (away_team, home_team)]
        print("Week\tAway Team\t@\tHome Team")
        for week, away_team, home_team in team_schedule:
            if away_team == team_name:
                print(f"{week}\t{away_team} (Away)\t@\t{home_team} (Home)")
            else:
                print(f"{week}\t{home_team} (Home)\t@\t{away_team} (Away)")

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
                    #print("Stadium: " + k + " (" + str(i) + ")")
                    return ("Stadium: " + k + " (" + str(i) + ")")
            else:
                #print("Stadium: " + k + " (" + str(v.get("Team")) + ")")
                #print("Team: " + str(v.get("Team")))
                if v.get("Team") == t:
                    return(k)
                 
class Game:
    def __init__(self, home_team, away_team):
        # what makes a game (teams, score, play time etc)
        self.home_team = home_team # pass in home team
        self.away_team = away_team # pass in away team
        self.league = League() # create league obj - has the get init league, get_stadium functions
        self.home_score = 0 # variable to track home team score
        self.away_score = 0 # variable to track away team score
        self.time = 60 # variable to track 60 minute games (have to work out how I fast I want to run the game)
        self.quaters = 4 # 4 quaters to a game

    def __repr__(self):
        return f"{self.away_team} @ {self.home_team} in {self.league.get_stadium(self.home_team)}"
    
    def match_day(self):
        '''Start the chosen Game. Clocks, sides, etc'''
        #if self.home_team == YOUR_TEAM : need a variable to hold the players team. Not sure how to implement yet.
        pass

    def play_quater(self):
        while self.time <= 15:
            # logic for game (has kick off been) - then into play selection
            # can be formation based, play based, like madden.
            # might create another function for actual game logic, keeping this as a timer func
            import datetime
            self.time -= datetime.timedelta(seconds=50)
            print(self.time)
        

    def coin_toss(self, player_team):
        if self.home_team == player_team:   
            cointoss = input("Heads or Tails? ").lower()
            flip_coin = random.randint(0, 1)
            if cointoss == flip_coin:
                play = input("Kick, Receive, or Defer? ").lower()
                if play == "kick":
                    direction = input("Pick a direction to kick L or R: ").lower()
                elif play == "receive":
                    direction = input("Pick a side to receive from L or R: ").lower()
                elif play == "defer":
                    pass
        
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


    l = League()
    schedule = l.generate_schedule()
    l.print_schedule(schedule)
    l.print_team_schedule("Green Bay Packers", schedule)

    #new_game = Game('Green Bay Packers', 'NY Jets')
    #print(new_game)
    