from core.league import League
from core.team import Team
import random

class Game:
    def __init__(self, home_team, away_team):
        # Expecting Team objects for home_team and away_team
        self.home_team = home_team
        self.away_team = away_team
        self.league = League()
        self.home_score = 0
        self.away_score = 0
        self.current_quarter = 1
        self.total_quarters = 4
        self.time_per_quarter = 15  # minutes per quarter
        self.time_remaining = self.time_per_quarter
        self.game_log = []  # For tracking plays/drives
        self.drives = []    # List of dicts for each drive
        self.plays = []     # List of dicts for each play
        self.possessions = []  # Track which team had the ball

    def __repr__(self):
        return f"{self.away_team.name} @ {self.home_team.name} in {self.league.get_stadium(self.home_team.name)}"

    def play_game(self):
        """Simulate the full game, quarter by quarter."""
        for q in range(1, self.total_quarters + 1):
            self.current_quarter = q
            self.time_remaining = self.time_per_quarter
            print(f"Quarter {q} begins!")
            self.play_quarter(q)
        print(f"Final Score: {self.home_team.name} {self.home_score} - {self.away_team.name} {self.away_score}")
        print("Game Log:")
        for log in self.game_log:
            print(log)

    def play_quarter(self, quarter):
        """Simulate a quarter with basic drive and play tracking."""
        print(f"Simulating Quarter {quarter}...")
        # Example: simulate 3 drives per quarter
        for drive_num in range(1, 4):
            offense = self.home_team if random.random() < 0.5 else self.away_team
            defense = self.away_team if offense == self.home_team else self.home_team
            drive_result = self.simulate_drive(offense, defense, quarter, drive_num)
            self.drives.append(drive_result)
            self.game_log.append(
                f"Q{quarter} Drive {drive_num}: {offense.name} - {drive_result['result']}"
            )
            # Update score
            if drive_result['result'] == 'TD':
                if offense == self.home_team:
                    self.home_score += 7
                else:
                    self.away_score += 7
            elif drive_result['result'] == 'FG':
                if offense == self.home_team:
                    self.home_score += 3
                else:
                    self.away_score += 3

    def simulate_drive(self, offense, defense, quarter, drive_num):
        """Simulate a single drive and return its result."""
        # Example: Each drive has 3-6 plays
        num_plays = random.randint(3, 6)
        result = random.choices(['TD', 'FG', 'Punt', 'Turnover'], weights=[0.3, 0.2, 0.4, 0.1])[0]
        drive = {
            'quarter': quarter,
            'drive_num': drive_num,
            'offense': offense.name,
            'defense': defense.name,
            'num_plays': num_plays,
            'result': result
        }
        # Track each play (placeholder)
        for play_num in range(1, num_plays + 1):
            play_result = self.simulate_play(offense, defense, quarter, drive_num, play_num)
            self.plays.append(play_result)
        self.possessions.append(offense.name)
        return drive

    def simulate_play(self, offense, defense, quarter, drive_num, play_num):
        """Simulate a single play (placeholder logic)."""
        play_types = ['Run', 'Pass', 'Sack', 'Incomplete', 'Penalty']
        play_type = random.choice(play_types)
        yards = random.randint(-5, 30) if play_type in ['Run', 'Pass'] else 0
        play = {
            'quarter': quarter,
            'drive_num': drive_num,
            'play_num': play_num,
            'offense': offense.name,
            'defense': defense.name,
            'type': play_type,
            'yards': yards
        }
        return play

    def match_day(self):
        # Placeholder for match day logic.
        pass

    def coin_toss(self, player_team):
        """Simulate a coin toss and let the player choose if they are the home team."""
        if self.home_team == player_team:
            cointoss = input("Heads or Tails? ").lower()
            flip_coin = "heads" if random.randint(0, 1) == 0 else "tails"
            if cointoss == flip_coin:
                play = input("You won the coin toss! Do you want to Kick, Receive, or Defer? ").lower()
                if play == 'kick':
                    direction = input("Pick a direction to kick Left or Right: ").lower()
                elif play == 'receive':
                    direction = input("Pick a side to receive Left or Right: ").lower()
                elif play == 'defer':
                    print("You chose to defer the kick. The opponent will receive the ball first.")
            else:
                print("You lost the coin toss. The opponent will choose to kick or receive first.")
        else:
            print("Opponent is the home team. They get to pick the coin toss options.")