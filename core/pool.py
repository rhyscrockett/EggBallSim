class Pool:
    def __init__(self):
        self.players = []

    def add(self, player):
        self.players.append(player)

    def print_pool(self):
        for player in self.players:
            print(f"{player.name} - {player.position} - ${player.price}")

    def find_player(self, name):
        for player in self.players:
            if player.name == name:
                print(f"Found: {player.name} - {player.position} - ${player.price}")
                return player
        print("Player not found.")
        return None

    def delete(self, name):
        player = self.find_player(name)
        if player:
            self.players.remove(player)
            print(f"Deleted {player.name}")