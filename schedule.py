import csv
from tabulate import tabulate

class Team:
    def __init__(self, name, abbreviation, conference, division):
        self.name = name
        self.abbreviation = abbreviation
        self.conference = conference
        self.division = division

class League:
    def __init__(self):
        self.teams = []
        self.load_teams_from_csv("teams.csv")

    def load_teams_from_csv(self, file_path):
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                team = Team(row['Team'], row['Abbreviation'], row['Conference'], row['Division'])
                self.teams.append(team)

    def get_teams_by_conference(self, conference):
        return [team for team in self.teams if team.conference == conference]

    def get_teams_by_division(self, conference, division):
        # Filter teams based on conference parameter
        conference_teams = self.get_teams_by_conference(conference)

        # Further filter teams by division
        return [team for team in conference_teams if team.division == division]

    def print_all_teams(self):
        table_data = []
        for team in self.teams:
            table_data.append([team.name, team.abbreviation, team.conference, team.division])

        print(tabulate(table_data, headers=['Name', 'Abbreviate', 'Conference', 'Division']))


if __name__ == '__main__':
    nfl = League()
    nfl.print_all_teams()
    afc = nfl.get_teams_by_conference('AFC')
    print("AFC Teams:")
    for team in afc:
        print(f"{team.name} ({team.abbreviation}) -  {team.conference} {team.division}")
        
    nfc_east = nfl.get_teams_by_division('NFC', 'East')
    print("\nNFC East Teams:")
    for team in nfc_east:
        print(f"{team.name} ({team.abbreviation}) - {team.conference} {team.division}")
