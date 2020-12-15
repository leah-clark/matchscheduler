class Squad:
    def __init__(self, name, hours, shift_time):
        self.name = name
        self.games = []
        self.hours = hours
        self.preferences = []
        self.shift_time = shift_time

    def add_preference(self, competition):
        self.preferences.append(competition)

    def add(self, game):
        self.games.append(game)

    def get_game_ids(self):
        game_ids = []
        for game in self.games:
            game_ids.append(game.game_id)
        return game_ids