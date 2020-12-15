class Game:
    def __init__(self, competition, game_id, deadline):
        self.competition = competition
        self.game_id = game_id
        self.is_assigned = False
        self.deadline = deadline
