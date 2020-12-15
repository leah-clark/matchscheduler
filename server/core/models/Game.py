class Game:
    def __init__(self, competition, game_id, deadline):
        self.competition = competition
        self.game_id = game_id
        self.is_assigned = False
        self.deadline = deadline
        self.squad = None

    def assign_game(self, squad):
        self.is_assigned = True
        self.squad = squad
