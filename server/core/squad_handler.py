from models.Squad import Squad
from operator import attrgetter
import logging

# todo: get these from data rather than hard coded
squad_letters = ['B+', 'E', 'D+', 'G', 'D', 'B', 'C', 'A']

logger = logging.getLogger("SquadHandler")


class SquadHandler:

    def __init__(self, squads_df):
        self.squads_df = squads_df
        self.squads = []

    def populate_squads(self, shift_time, squad_preferences):
        available_squads = self.squads_df.loc[self.squads_df['Date'] == shift_time]
        for letter in squad_letters:
            squad = Squad(name=letter, hours=available_squads[letter].values[0], shift_time=shift_time)
            squad.preferences = squad_preferences[letter]
            self.squads.append(squad)

    def _find_squad_with_most_hours(self):
        return max(self.squads, key=attrgetter('hours'))

    def get_preferred_squad(self, game):
        for squad in self.squads:
            if game.competition in squad.preferences:
                return squad
        return None

    def reassign_game(self, game):
        squad = self._find_squad_with_most_hours()
        logger.info("Squad: " + str(squad.name))
        if squad.hours > 10:
            self.add_game_to_schedule(10, squad, game)
            game.is_assigned = True

    def add_game_to_schedule(self, time_taken, squad, game):
        squad.add(game)
        logger.info("Game added to schedule... ")
        squad.hours -= time_taken
        game.is_assigned = True
