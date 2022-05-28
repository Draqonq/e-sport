from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from classes import Tournament, Round, Fight, Team
import random
import math

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://Piorob:Robpio@cluster0.cftar.mongodb.net/serwisy?retryWrites=true&w=majority'
mongo = PyMongo(app)
teams = mongo.db.teams

#Tournament and registered teams
tournament_name = "Chess Master"
tournament_description = "W turnieju mogą wziąć udział studenci informatyki stosowanej oraz teleinformatyki. Liczymy na zwycięztwo informatyków!"

#registered_teams = ["Alakonda", "Mojowojo", "TeamXD", "Bałkan", "WODOGRZOM"]
registered_teams = []
tournament = Tournament(tournament_name, registered_teams)

#Rounds and winner
current_round = 0
rounds = []
number_of_rounds = 0

winner = ""

button_winner_team = []
button_winner_fight = []

#Pre start
def add_to_registered_teams(team):
    global registered_teams
    if not team in registered_teams and len(team) > 0 and len(team) < 11:
        team_item = Team(team)
        registered_teams.append(team_item)

def add_member_to_registered_teams(member, team):
    global registered_teams
    for teams in registered_teams:
        if teams == team:
            teams.add_member(member)

#Start game
def start_game():
    global rounds
    global number_of_rounds
    round = Round("Round "+str(current_round), tournament.teams)
    rounds.append(round)

    # for x in rounds[0].teams:
    #     print(x)
        
    #Other rounds (Empty)
    number_of_rounds = count_number_of_rounds()
    for i in range(current_round + 1, number_of_rounds):
        rounds.append(Round("Round "+str(i),[]))
    #First fights (Random fights)
    rounds[current_round].fights = random_fight()

def count_number_of_rounds():
    global registered_teams
    number_of_player = len(registered_teams)
    number_of_rounds = 0
    while number_of_player > 1:
        number_of_rounds += 1
        number_of_player = math.ceil(number_of_player/2)
    return number_of_rounds

#Fights => {fight{team, team}, fight{team, team}}
def random_fight():
    global rounds
    global current_round
    if current_round == 0:
        teams = tournament.teams[:]
    else:
        teams = rounds[current_round-1].winners[:]
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
        fight_object = Fight(fight)
        rounds[current_round].add_fight(fight_object)
        fights.append(fight)
    return fights

#Round winner
def add_winner_to_list(item):
    global button_winner_team
    global button_winner_fight
    global rounds
    item = item.split(",")
    winner = item[0]
    fight = item[1]
    if not winner in button_winner_team and not fight in button_winner_fight:
        button_winner_team.append(winner)
        button_winner_fight.append(fight)
        add_round_winner(winner)
        check_round()

def add_round_winner(winner):
    global current_round
    global rounds

    # for x in rounds[current_round].teams:
    #     print(x)

    item = next((i for i in rounds[current_round].teams if i == winner), None)
    rounds[current_round].add_winner(item)

def fill_next_round():
    global current_round
    global button_winner_team
    global button_winner_fight

    button_winner_team = []
    button_winner_fight = []
    rounds[current_round].teams = rounds[current_round-1].winners
    rounds[current_round].fights = random_fight()

def check_round():
    global number_of_rounds
    global current_round
    global rounds
    #Number of winners
    round_winners = len(rounds[current_round].winners)
    #Number of fights
    round_fights = len(rounds[current_round].fights)

    # round_fight = len(rounds[current_round].teams)
    # print(round_fight)

    if(round_fights != 0 and current_round + 1 < number_of_rounds and round_winners >= round_fights):
        current_round += 1
        fill_next_round()
        print("Następna runda")
    elif(round_fights != 0 and current_round + 1 >= number_of_rounds):
        global winner
        winner = str(rounds[current_round].winners[0])

    # if(round_fight != 0 and current_round + 1 < number_of_rounds and round_winners >= round_fight):
    #     current_round += 1
    #     fill_next_round()
    #     button_winner_team = []
    #     #print("Następna runda")
    # elif(round_fight != 0 and current_round + 1 >= number_of_rounds):
    #     #wingame
    #     global winner
    #     winner = rounds[current_round].winners[0]
    #     button_winner_team = []

@app.route('/')
def index():
    #saved_todos = teams.find()
    #teams.insert_one({'teams' : 'xddd'})
    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description, registered_teams=registered_teams, rounds=rounds, current_round=current_round, winner=winner)

@app.route('/', methods=['POST'])
def index2():
    if request.form.get('team'):
        add_winner_to_list(request.form.get('team'))
    elif request.form.get('manageTeams'):
        if request.form.get('player') and request.form.get('manageTeams') == "addPlayer":
            add_to_registered_teams(request.form.get('player'))
        elif request.form.get('manageTeams') == "blockAddPlayer":
            start_game()
    elif request.form.get('member'):
        #print(request.form.get('memberName'))
        #print(request.form.get('memberTeam'))
        add_member_to_registered_teams(request.form.get('memberName'), request.form.get('memberTeam'))
        #Add team member
    elif request.form.get('reset'):
        print("reset")

    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description, registered_teams=registered_teams, rounds=rounds, current_round=current_round, winner=winner)

#Registered teams





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
