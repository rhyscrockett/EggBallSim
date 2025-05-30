from tabulate import tabulate
import random
from core.team import Team
from utils.fileio import read_csv, read_json

class League:
    def __init__(self):
        self.teams = []
        self.nfc = {}
        self.afc = {}
        self.load_teams_from_csv("teams.csv")

    def load_teams_from_csv(self, file_path):
        rows = read_csv(file_path)
        for row in rows:
            team = Team(row['Team'], row['Abbreviation'], row['Conference'], row['Division'])
            self.teams.append(team)
            if team.conference == "NFC":
                self.nfc.setdefault(team.division, []).append(team.name)
            elif team.conference == "AFC":
                self.afc.setdefault(team.division, []).append(team.name)

    def get_teams_by_conference(self, conference):
        return [team for team in self.teams if team.conference == conference]

    def get_teams_by_division(self, conference, division):
        return [team for team in self.teams if team.conference == conference and team.division == division]

    def print_all_teams(self):
        table_data = [[team.name, team.abbreviation, team.conference, team.division] for team in self.teams]
        print(tabulate(table_data, headers=['Name', 'Abbreviation', 'Conference', 'Division']))

    def get_stadium(self, team_name):
        stadiums = read_json("stadiums.json")
        return stadiums.get(team_name, "Unknown Stadium")

    def generate_schedule(self):
        '''
        Generate a schedule for the current Game league.
        '''
        # 1. Six games against divisional opponents (should return 96 games)
        division_matchups = [] # Divisional games (NFC West, NFC North, etc.)
        for division in self.nfc.values():
            division_matchups.extend(self._generate_divisional_matchups(division))
        for division in self.afc.values():
            division_matchups.extend(self._generate_divisional_matchups(division))

        # 2. Four games against teams from a division within its conference (should return 64 games)
        conference_matchups = self._generate_conference_matchups()
        # 3. Four games against teams from a division in the other conference (should return 64 games)
        interconference_matchups = self._generate_interconference_matchups()

        # 4. Two games against teams from the same divisional rank in each of the two intraconference divisions (should return 32 games)
        nfc_parity = self._generate_parity_matchups(
            self._identify_remaining_divisions(conference_matchups, self.nfc), self.nfc)
        afc_parity = self._generate_parity_matchups(
            self._identify_remaining_divisions(conference_matchups, self.afc), self.afc)

        # 5. The 17th game is an additional game against a non-conference opponent from a division that the team is not scheduled to play. Matchups are based on division ranking from the previous season. (should return 16 games - WIP)

        # 6. Assign Bye weeks to teams (WIP).

        schedule = conference_matchups + division_matchups + interconference_matchups + nfc_parity + afc_parity
        random.shuffle(schedule) # Shuffle the schedule to randomize matchups.
        return schedule

    def _generate_conference_matchups(self):
        matchups = []
        for conf in [self.nfc, self.afc]:
            divisions = list(conf.values())
            random.shuffle(divisions)
            for div1, div2 in zip(divisions[0::2], divisions[1::2]):
                matchups.extend(self._generate_home_away_matchups(div1, div2))
        return matchups

    def _generate_home_away_matchups(self, teams1, teams2):
        """Helper for generating 2 home and 2 away games for each team."""
        matchups = []
        for team in teams1:
            opponents = list(teams2)
            home = random.sample(opponents, 2)
            opponents = [t for t in opponents if t not in home]
            away = random.sample(opponents, 2)
            for opp in home:
                matchups.append((team, opp))
            for opp in away:
                matchups.append((opp, team))
        return matchups

    
    def _generate_divisional_matchups(self, division_teams):
        """Each team plays every other team in its division twice (home and away)."""
        matchups = []
        for i in range(len(division_teams)):
            for j in range(i + 1, len(division_teams)):
                matchups.append((division_teams[i], division_teams[j])) 
                matchups.append((division_teams[j], division_teams[i]))
        random.shuffle(matchups)
        return matchups

    def _generate_interconference_matchups(self):
        matchups = []
        nfc_divs = list(self.nfc.values())
        afc_divs = list(self.afc.values())
        random.shuffle(afc_divs)
        for nfc_div, afc_div in zip(nfc_divs, afc_divs):
            matchups.extend(self._generate_home_away_matchups(nfc_div, afc_div))
        return matchups

    def _generate_parity_matchups(self, parity_matchups, conference_teams):
        matchups = []
        for div1, div2 in parity_matchups:
            teams1 = conference_teams[div1]
            teams2 = conference_teams[div2]
            for rank in range(min(len(teams1), len(teams2))):
                if random.choice([True, False]):
                    matchups.append((teams1[rank], teams2[rank]))
                else:
                    matchups.append((teams2[rank], teams1[rank]))
        return matchups
    
    def _identify_remaining_divisions(self, division_matchups, conference_teams):
        paired_divisions = set()
        for home, away in division_matchups:
            home_div = away_div = None
            for division, teams in conference_teams.items():
                if home in teams:
                    home_div = division
                if away in teams:
                    away_div = division
            if home_div and away_div:
                paired_divisions.add(tuple(sorted((home_div, away_div))))
        remaining = list(conference_teams.keys())
        parity_pairs = set()
        for d1 in remaining:
            for d2 in paired_divisions:
                if d1 != d2[0] and d1 != d2[1]:
                    parity_pairs.add(tuple(sorted((d1, d2[0]))))
                    parity_pairs.add(tuple(sorted((d1, d2[1]))))
        return parity_pairs
    
    def print_schedule(self, schedule):
        """Prints the schedule in a clean, readable format."""
        print(f"{'Week':<5} {'Away Team':<25} @ {'Home Team':<25}")
        for week, (away_team, home_team) in enumerate(schedule, start=1):
            print(f"{week:<5} {away_team:<25} @ {home_team:<25}")

    def print_team_schedule(self, team_name, schedule):
        """Prints the schedule for a specific team with correct week numbers."""
        print(f"Schedule for {team_name}:")
        print(f"{'Week':<5} {'Opponent':<25} {'Location':<10}")
        week_num = 1
        for away_team, home_team in schedule:
            away_name = away_team.name if hasattr(away_team, 'name') else away_team
            home_name = home_team.name if hasattr(home_team, 'name') else home_team
            if team_name == home_name:
                opponent = away_name
                location = "Home"
            elif team_name == away_name:
                opponent = home_name
                location = "Away"
            else:
                continue
            print(f"{week_num:<5} {opponent:<25} {location:<10}")
            week_num += 1

    def print_league(self):
        """Prints all conferences and divisions in the league."""
        for conf_name, conf in [('NFC', self.nfc), ('AFC', self.afc)]:
            print(f"\nConference: {conf_name}")
            for division, teams in conf.items():
                print(f"  {division}: {', '.join(teams)}")

    def match_division(self, t):
        '''Take a team as a parameter to find their conference and division'''
        for conf, div in self.league.items():
            for zone, team in div.items():
                if t in team:
                    return conf, zone
                else:
                    continue
        return None