import random
import names

class Player:
    '''
    Represents a football player with position-based attributed and skills.
    '''
    def __init__(self, name, position, price, age=None, experience=None):
        self.name = name
        self.position = position
        self.price = price
        self.age = age if age is not None else random.randint(21, 38)
        self.experience = experience if experience is not None else random.randint(0, self.age - 20)
        self.injury_status = "Healthy"
        self.morale = random.randint(50, 100)
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
        stats = (
            f"STR: {self.strength}\tSTA: {self.stamina}\tSPD: {self.speed}\t"
            f"AGL: {self.agility}\tACC: {self.accuracy}\n"
            f"Age: {self.age}\tExperience: {self.experience}\tMorale: {self.morale}\tInjury Status: {self.injury_status}"
        )
        return f"{self.name}: ({self.position}) - {price}\n{stats}"

    @staticmethod
    def generate_position():
        """Returns a random position from a list of possible player positions."""
        pos = ["QB", "RB", "WR", "TE", "LT", "LG", "C", "RG", "RT",
               "DT", "DE", "MLB", "OLB", "CB", "SS", "FS",
               "K", "P"]
        return random.choice(pos)

    @staticmethod
    def generate_name():
        """Returns a random name from the names library."""
        return names.get_full_name(gender='male')
    
    @staticmethod
    def generate_price():
        """Returns a random float value rounded to the closes."""
        base = 660_000
        top = 50_000_000
        return round(random.uniform(base, top))