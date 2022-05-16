from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import random
import math

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://Piorob:Robpio@cluster0.cftar.mongodb.net/serwisy?retryWrites=true&w=majority'
mongo = PyMongo(app)

teams = mongo.db.teams

class Tournament:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

class Round:
    winners = []
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

class Fight:
    def __init__(self, teams):
        self.teams = teams

def random_fight(round):
    teams = round.teams
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

def add_winner(rounds, current_round, winner):
    rounds[current_round].winners.append(winner)
    #print(rounds[current_round].winners)
    return check_round(rounds, current_round)

def check_round(rounds, current_round):
    round_winners = len(rounds[current_round].winners)
    #print(round_winners)
    round_players = len(rounds[current_round].teams)
    #print(round_players)
    if(round_players != 0 and round_winners >= round_players):
        current_round += 1
        fill_next_round(rounds, current_round)
        #print("Następna runda")
    return current_round

def fill_next_round(rounds, current_round):
    rounds[current_round].teams = rounds[current_round-1].winners
    rounds[current_round].teams = random_fight(rounds[current_round])


#Tournament and registered teams
tournament_name = "Chess Master"
tournament_description = "W turnieju mogą wziąć udział studenci informatyki stosowanej oraz teleinformatyki. Liczymy na zwycięztwo informatyków!"
registered_teams = ["Alakonda", "Mojowojo", "TeamXD", "Bałkan", "WODOGRZOM"]
tournament = Tournament(tournament_name, registered_teams)
#First round
current_round = 0
round = Round("Round "+str(current_round), tournament.teams)
rounds = [round]
#Other rounds (Empty)
number_of_rounds = number_of_rounds(registered_teams)
for i in range(current_round + 1, number_of_rounds):
    rounds.append(Round("Round "+str(i),[]))
#First fights (Random fights)
rounds[current_round].teams = random_fight(rounds[current_round])

#print(rounds[current_round].teams)

# current_round = add_winner(rounds, current_round, "Mojowojo")
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
    saved_todos = teams.find()
    #teams.insert_one({'teams' : 'xddd'})
    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description, rounds=rounds)

testlist = []

def addlist(item):
    if not item in testlist:
        testlist.append(item)


@app.route('/', methods=['POST'])
def index2():
    #saved_todos = teams.find()
    #teams.insert_one({'teams' : 'xddd'})
    print(request.form.get('team'))
    addlist(request.form.get('team'))
    print(testlist)
    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description, rounds=rounds)