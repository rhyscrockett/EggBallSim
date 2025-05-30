class Team:
    def __init__(self, name, abbreviation, conference, division):
        self.name = name
        self.abbreviation = abbreviation
        self.conference = conference
        self.division = division
        self.roster = [] # List if Player objects
        self.injured_players = []
        self.salary_cap = 208_200_000 # Example NFL salary cap.
        self.current_payroll = 0
        self.season_stats = {
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'points_for': 0,
            'points_against': 0,
        }
        self.game_stats = [] # List of dicts for each game.

    def add_player(self, player):
        """Adds a Player to the team's roster."""
        self.roster.append(player)

    def remove_player(self, player_name):
        """Remove a Player by name from the roster."""
        for player in self.roster:
            if player.name.lower() == player_name.lower():
                self.roster.remove(player)
                return True
        return False
    
    def find_player(self, player_name):
        """Find a Player by name."""
        for player in self.roster:
            if player.name.lower() == player_name.lower():
                return player
        return None
    
    def is_roster_valid(self):
        # Check for 53 players, position minimums, etc.
        pass

    def get_depth_chart(self):
        # Returns Players grouped and sorted by position.
        pass

    def add_to_injured_reserve(self, player):
        # Move player from roster to IR.
        pass

    def can_afford(self, player):
        # Check if adding player exceeds salary cap.
        pass

    def record_game_stats(self, game_stats):
        # Add a game's stats to the team's history.
        self.game_stats.append(game_stats)
    
    def __repr__(self):
        return f"{self.name} ({self.abbreviation}) - {self.conference} {self.division} | Roster Size: {len(self.roster)}"
    