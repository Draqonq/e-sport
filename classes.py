from operator import truediv


class Tournament:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        self.winner = None

    def add_team(self, team):
        self.teams.append(team)

    def add_winner(self, winner):
        self.winner = winner

class Round:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        self.winners = []
        self.fights = []
    
    def add_fight(self, fight):
        self.fights.append(fight)
        
    def add_winner(self, winner):
        self.winners.append(winner)

class Fight:
    def __init__(self, teams):
        self.teams = teams

class Team:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        else:
            return self.name == other.name
