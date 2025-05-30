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
        conference_teams = self.get_teams_by_conference(conference)
        return [team for team in conference_teams if team.division == division]

    def print_all_teams(self):
        table_data = []
        for team in self.teams:
            table_data.append([team.name, team.abbreviation, team.conference, team.division])
        print(tabulate(table_data, headers=['Name', 'Abbreviation', 'Conference', 'Division']))

    def get_stadium(self, team_name):
        stadiums = read_json("stadiums.json")
        return stadiums.get(team_name, "Unknown Stadium")

    def generate_schedule(self): # (NOT INCLUDING BYE) 256/272
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

        # 4. Two games against teams from the same divisional rank in each of the two intraconference divisions (returns 32 games!)
        nfc_remaining_matchups = self._identify_remaining_divisions(conference_matchups, self.nfc)
        afc_remaining_matchups = self._identify_remaining_divisions(conference_matchups, self.afc)
        nfc_parity_matchups = self._generate_parity_matchups(nfc_remaining_matchups, self.nfc)
        afc_parity_matchups = self._generate_parity_matchups(afc_remaining_matchups, self.afc)

        all_parity_matchups = nfc_parity_matchups + afc_parity_matchups
        parity_matchups.extend(all_parity_matchups)

        # 5. The 17th game is an additional game against a non-conference opponent from a division that the team is not scheduled to play. Matchups are based on division ranking from the previous season. (should return 16 games - WIP)


        schedule = conference_matchups + division_matchups + interconference_matchups + parity_matchups

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

    def _identify_remaining_divisions(self, division_matchups, conference_teams):
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
                paired_divisions.add(tuple(sorted((home_team_division, away_team_division))))

        remaining_divisions = list(conference_teams.keys())
        parity_division_pairs = set()

        for division1 in remaining_divisions:
            for division2 in paired_divisions:
                if division1 != division2[0] and division1 != division2[1]:
                    parity_division_pairs.add(tuple(sorted((division1, division2[0]))))
                    parity_division_pairs.add(tuple(sorted((division1, division2[1]))))

        #print("Previous paired matchups:")
        #for division_pair in paired_divisions:
        #    print(f"{division_pair}")

        #print("New Paired divisions:")
        #for division_pair in parity_division_pairs:
        #    print(f"{division_pair}")

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


    def _generate_parity_matchups(self, parity_matchups, conference_teams):
        matchups = []
    
        for division1, division2 in parity_matchups:
            division1_teams = conference_teams[division1]
            division2_teams = conference_teams[division2]

            for rank in range(len(division1_teams)):
                team1 = division1_teams[rank]
                team2 = division2_teams[rank]

                if random.choice([True, False]):
                    matchups.append((team1, team2))
                else:
                    matchups.append((team2, team1))

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