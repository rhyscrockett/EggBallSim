from core.league import League
from core.team import Team
from core.player import Player
from core.pool import Pool
from core.game import Game

if __name__ == '__main__':
    def generate_players():
        """Returns a Pool object that contains a pool of randomly generated players."""
        player_pool = Pool()
        for _ in range(100):
            p = Player(Player.generate_name(), Player.generate_position(), Player.generate_price())
            player_pool.add(p)
        return player_pool
    
    players = generate_players()
    players.print_pool()
    players.find_player("Rhys Crockett")
    players.delete("Rhys Crockett")

    l = League()
    schedule = l.generate_schedule()
    # l.print_schedule(schedule)  # Uncomment if implemented
    # l.print_team_schedule("Green Bay Packers", schedule)  # Uncomment if implemented

    # new_game = Game('Green Bay Packers', 'NY Jets')
    # print(new_game)
