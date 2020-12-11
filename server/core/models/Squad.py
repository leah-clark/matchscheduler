class Squad:
    def __init__(self, name, hours, shift_time):
        self.name = name
        self.match_ids = []
        self.hours = hours
        self.preferences = []
        self.shift_time = shift_time

    def add_preference(self, competition):
        self.preferences.append(competition)

    def add_match_id(self, id):
        self.match_ids.append(id)