from core.league import League
import random

class Game:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.league = League()
        self.home_score = 0
        self.away_score = 0
        self.time = 60  # minutes remaining
        self.quarters = 4  # fixed typo

    def __repr__(self):
        return f"{self.away_team} @ {self.home_team} in {self.league.get_stadium(self.home_team)}"
    
    def match_day(self):
        pass

    def play_quarter(self):
        while self.time > 0:
            # Simulate time passing (e.g., 15 minutes per quarter)
            self.time -= 15
            print(f"Time remaining: {self.time} minutes")
        

    def coin_toss(self, player_team):
        if self.home_team == player_team:   
            cointoss = input("Heads or Tails? ").lower()
            flip_coin = "heads" if random.randint(0, 1) == 0 else "tails"
            if cointoss == flip_coin:
                play = input("Kick, Receive, or Defer? ").lower()
                if play == "kick":
                    direction = input("Pick a direction to kick L or R: ").lower()
                elif play == "receive":
                    direction = input("Pick a side to receive from L or R: ").lower()
                elif play == "defer":
                    pass