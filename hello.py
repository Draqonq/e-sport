from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import random
import math

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://Piorob:Robpio@cluster0.cftar.mongodb.net/serwisy?retryWrites=true&w=majority'
mongo = PyMongo(app)
teams = mongo.db.teams

class Tournament:
    def __init__(self, name):
        self.name = name
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

    def add_team(self, team):
        self.teams.append(team)

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

def random_fight(round):
    teams = round.teams[:]
    fights = []
    for i in range(math.ceil(len(teams)/2)):
        fight = []
        teamName = random.choice(teams)
        fight.append(teamName)
        teams.remove(teamName)
        if len(teams) > 0:
            teamName = random.choice(teams)
            fight.append(teamName)
            teams.remove(teamName)
        fights.append(fight)
    return fights
        
def number_of_rounds(teams):
    number_of_player = len(teams)
    number_of_rounds = 0
    while number_of_player > 1:
        number_of_rounds += 1
        number_of_player = math.ceil(number_of_player/2)
    return number_of_rounds

#del current_round
#del rounds
def add_winner(winner):
    global current_round
    global rounds
    #rounds[current_round].winners.append(winner)
    rounds[current_round].add_winner(winner)
    print("runda" + str(current_round))
    print(rounds[current_round].winners)
    for r in rounds:
        print(r.winners)
    return check_round()

#del current_round
#del rounds
def check_round():
    global number_of_rounds
    global button_winner_team
    global current_round
    global rounds
    round_winners = len(rounds[current_round].winners)
    #print(round_winners)
    round_fight = len(rounds[current_round].teams)
    #print(round_fight)
    if(round_fight != 0 and current_round+1 < number_of_rounds and round_winners >= round_fight):
        current_round += 1
        fill_next_round()
        button_winner_team = []
        #print("Następna runda")
    elif(round_fight != 0 and current_round+1 >= number_of_rounds):
        #wingame
        global winner
        winner = rounds[current_round].winners[0]
        button_winner_team = []
    return current_round

#del current_round
#del rounds
def fill_next_round():
    global current_round
    rounds[current_round].teams = rounds[current_round-1].winners
    rounds[current_round].teams = random_fight(rounds[current_round])


#Tournament and registered teams
tournament_name = "Chess Master"
tournament_description = "W turnieju mogą wziąć udział studenci informatyki stosowanej oraz teleinformatyki. Liczymy na zwycięztwo informatyków!"
registered_teams = ["Alakonda", "Mojowojo", "TeamXD", "Bałkan", "WODOGRZOM"]
tournament = Tournament(tournament_name, registered_teams)
#First round
current_round = 0
winner = ""
rounds = []
number_of_rounds

def start_game():
    global rounds
    global number_of_rounds
    round = Round("Round "+str(current_round), tournament.teams)
    rounds = [round]
    #Other rounds (Empty)
    number_of_rounds = number_of_rounds(registered_teams)
    for i in range(current_round + 1, number_of_rounds):
        rounds.append(Round("Round "+str(i),[]))
    #First fights (Random fights)
    rounds[current_round].teams = random_fight(rounds[current_round])
#print(rounds[current_round].teams)

#current_round = add_winner(rounds, current_round, "Mojowojo")
# current_round = add_winner(rounds, current_round, "TeamXD")
# current_round = add_winner(rounds, current_round, "Bałkan")

# print(rounds[current_round].teams)


# round0_winners = ["Mojowojo", "Bałkan", "WODOGRZOM"]
# round[0].winners = round0_winners

# round_winners = len(round[0].winners)
# print(round_winners)
# round_players = len(round[0].teams)
# print(round_players)
# while(round_players != 0 and round_winners >= round_players):
#     print("Następna runda")
#     round_winners = len(round[1].winners)
#     round_players = len(round[1].teams)


@app.route('/')
def index():
    #saved_todos = teams.find()
    #teams.insert_one({'teams' : 'xddd'})
    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description, registered_teams=registered_teams, rounds=rounds, current_round=current_round, winner=winner)

button_winner_team = []
def addlist(item):
    if not item in button_winner_team:
        global current_round
        button_winner_team.append(item)
        current_round = add_winner(item)
        print("następna runda:"+str(current_round))

def add_to_registered_teams(item):
    global registered_teams
    if not item in registered_teams and len(item) > 0 and len(item) < 11:
        registered_teams.append(item)
        #tournament.add_team(item)
        #print(tournament.teams)



@app.route('/', methods=['POST'])
def index2():
    if request.form.get('team'):
        addlist(request.form.get('team'))
    elif request.form.get('manageTeams'):
        if request.form.get('player') and request.form.get('manageTeams') == "addPlayer":
            add_to_registered_teams(request.form.get('player'))
        elif request.form.get('manageTeams') == "blockAddPlayer":
            start_game()
    elif request.form.get('member'):
        print(request.form.get('memberName'))
        print(request.form.get('memberTeam'))
        #Add team member

    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description, registered_teams=registered_teams, rounds=rounds, current_round=current_round, winner=winner)
