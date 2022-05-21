class Tournament:
    def __init__(self, *args):
        if len(args) == 1:
            self.name = args[0]
        elif len(args) == 2:
            self.name = args[0]
            self.teams = args[1]
        elif len(args) == 3:
            self.name = args[0]
            self.teams2 = args[1]

    # def __init__(self, name):
    #     self.name = name
    # def __init__(self, name, teams):
    #     self.name = name
    #     self.teams = teams
        
    # def __init__(self, name, teams2, test2):
    #     self.name = name
    #     self.teams2 = teams2

    def add_team(self, team):
        self.teams.append(team)

    def add_winner(self, winner):
        self.winner = winner

    

    def add_team2(self, team2):
        self.teams2.append(team2)

class Round:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams
        self.winners = []
    
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
