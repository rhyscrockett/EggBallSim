class Pool:
    def __init__(self):
        self.players = []

    def add(self, player):
        """Adds a player to the pool."""
        self.players.append(player)

    def add_multiple(self, players):
        """Adds multiple players to the pool."""
        for player in players:
            self.players.extend(players)

    def print_pool(self, sort_by=None, position=None):
        '''
        Print all players in the pool.
        Optionally sort by an attribute (e.g., 'price', 'name', 'position').
        Optionally filter by position.
        '''
        players = self.players
        if position:
            players = [p for p in players if p.position == position]
        if sort_by:
            players = sorted(players, key=lambda p: getattr(p, sort_by))
        for player in players:
            print(f"{player.name} - {player.position} - ${player.price}")

    def find_player(self, name):
        """FInd a player by their name (case-insensitive)."""
        for player in self.players:
            if player.name.lower() == name.lower():
                print(f"Found: {player.name} - {player.position} - ${player.price}")
                return player
        print("Player not found.")
        return None

    def delete(self, name):
        """Deletes a player from the pool by name."""
        player = self.find_player(name)
        if player:
            self.players.remove(player)
            print(f"Deleted {player.name}")
            return True
        return False
    
    def delete_multiple(self, names):
        """Deletes multiple players by a list of names."""
        deleted = []
        for name in names:
            if self.delete(name):
                deleted.append(name)
        return deleted