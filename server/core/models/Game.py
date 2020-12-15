

class Game:
    def __init__(self, competition, game_id, deadline):
        self.competition = competition
        self.game_id = game_id
        self.is_assigned = False
        self.deadline = deadline
        self.Late = Late()

    def set_late_game(self, time_late):
        self.Late.is_late = True
        self.Late.time_late = time_late


class Late:
    def __init__(self):
        self.is_late = False
        self.time_late = None
