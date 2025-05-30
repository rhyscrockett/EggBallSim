from core.league import League
from core.team import Team
from core.player import Player
from core.pool import Pool
from core.game import Game

def generate_players(num_players=100):
    """Returns a Pool object that contains a pool of randomly generated players."""
    player_pool = Pool()
    for _ in range(num_players):
        p = Player(Player.generate_name(), Player.generate_position(), Player.generate_price())
        player_pool.add(p)
    return player_pool

if __name__ == '__main__':
    # Generate and display player pool
    players = generate_players()
    print("\n--- Player Pool (first 10) ---")
    players.print_pool(sort_by='price')

    # Add a known player
    known_player = Player("Rhys Crockett", "QB", 1_000_000)
    players.add(known_player)
    print("\nAdded player: Rhys Crockett (QB)")

    print("\nFind and delete a player:")
    players.find_player("Rhys Crockett")
    players.delete("Rhys Crockett")
    players.find_player("Rhys Crockett")  # Should now print "Player not found."

    # League and schedule
    league = League()
    print("\n--- All Teams ---")
    league.print_all_teams()
    print("\n--- League Structure ---")
    league.print_league()

    schedule = league.generate_schedule()
    print("\n--- Sample Schedule (first 10 games) ---")
    league.print_schedule(schedule[:10])

    # Demonstrate team schedule print
    team_name = "Green Bay Packers"
    print(f"\n--- {team_name} Schedule ---")
    league.print_team_schedule(team_name, schedule)

    # Simulate a game between two real teams
    home_team = next((t for t in league.teams if t.name == "Green Bay Packers"), None)
    away_team = next((t for t in league.teams if t.name == "Chicago Bears"), None)
    if home_team and away_team:
        print(f"\n--- Simulating Game: {away_team.name} @ {home_team.name} ---")
        game = Game(home_team, away_team)
        print(game)
        game.play_game()
    else:
        print("\nCould not find both teams for game simulation.")