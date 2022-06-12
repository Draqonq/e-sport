from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from classes import Tournament, Round, Fight, Team
import random
import math

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://Piorob:Robpio@cluster0.cftar.mongodb.net/esport?retryWrites=true&w=majority'
mongo = PyMongo(app)
mongo_members = mongo.db.members
mongo_teams = mongo.db.teams
mongo_winners = mongo.db.tournament_winners
# Tournament and registered teams
tournament_name = "PBŚ Valorant Champions"
tournament_description = "Turniej zorganizowany przez Wydział Telekomunikacji, Informatyki i Elektrotechniki. Wziąć w nim udział  mogą studenci Politechniki Bydgoskiej. Rozgrywane będą mecze w taktycznego FPS'a stworzonego przez Riot Games, grę Valorant"

registered_teams = []
tournament = Tournament(tournament_name, registered_teams)

# Rounds and winner
current_round = 0
rounds = []
number_of_rounds = 0

winner = ""

button_winner_team = []
button_winner_fight = []
selected_team = ""

def reset_all():
    global registered_teams
    global current_round
    global rounds
    global number_of_rounds
    global winner
    global button_winner_team
    global button_winner_fight
    global tournament
    global selected_team
    registered_teams = []
    current_round = 0
    rounds = []
    number_of_rounds = 0
    winner = ""
    button_winner_team = []
    button_winner_fight = []
    tournament = Tournament(tournament_name, registered_teams)
    selected_team = ""

# Pre start
def add_to_registered_teams(team):
    global registered_teams
    if not team in registered_teams and len(team) > 0 and len(team) < 11:
        team_item = Team(team)
        registered_teams.append(team_item)
        db_team = {"team_name": team_item.name, "team_members": []}
        mongo_teams.insert_one(db_team)


def add_member_to_registered_teams(member, team):
    global registered_teams
    global selected_team
    for teams in registered_teams:
        if teams == team:
            teams.add_member(member)
            selected_team = team
            db_member = {"member_name": member, "team_name": team}
            mongo_members.insert_one(db_member)


# Start game
def start_game():
    global rounds
    global number_of_rounds
    round = Round("Round " + str(current_round), tournament.teams)
    rounds.append(round)

    # Other rounds (Empty)
    number_of_rounds = count_number_of_rounds()
    for i in range(current_round + 1, number_of_rounds):
        rounds.append(Round("Round " + str(i), []))
    # First fights (Random fights)
    rounds[current_round].fights = random_fight()


def count_number_of_rounds():
    global registered_teams
    number_of_player = len(registered_teams)
    number_of_rounds = 0
    while number_of_player > 1:
        number_of_rounds += 1
        number_of_player = math.ceil(number_of_player / 2)
    return number_of_rounds


# Fights => {fight{team, team}, fight{team, team}}
def random_fight():
    global rounds
    global current_round
    if current_round == 0:
        teams = tournament.teams[:]
    else:
        teams = rounds[current_round - 1].winners[:]
    fights = []
    for i in range(math.ceil(len(teams) / 2)):
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


# Round winner
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
    item = next((i for i in rounds[current_round].teams if i == winner), None)
    rounds[current_round].add_winner(item)


def fill_next_round():
    global current_round
    global button_winner_team
    global button_winner_fight

    button_winner_team = []
    button_winner_fight = []
    
    rounds[current_round].teams = rounds[current_round - 1].winners
    rounds[current_round].fights = random_fight()


def check_round():
    global number_of_rounds
    global current_round
    global rounds
    # Number of winners
    round_winners = len(rounds[current_round].winners)
    # Number of fights
    round_fights = len(rounds[current_round].fights)

    if (round_fights != 0 and current_round + 1 < number_of_rounds and round_winners >= round_fights):
        current_round += 1
        fill_next_round()
    elif (round_fights != 0 and current_round + 1 >= number_of_rounds):
        global winner
        winner = str(rounds[current_round].winners[0])
        # db_winning_team = {"team_name": winner, "team_members": [winner.]}
        db_winning_members = list(mongo_members.find({"team_name": winner}))
        db_winning_team = {"team_name": winner, "team_members": db_winning_members}
        mongo_winners.insert_one(db_winning_team)


@app.route('/')
def index():
    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description,
                           registered_teams=registered_teams, rounds=rounds, current_round=current_round, winner=winner, selected_team=selected_team)


@app.route('/winners')
def tournament_winners():
    all_past_winners = list(mongo_winners.find({}))
    return render_template('winners.html', winners=all_past_winners)


@app.route('/', methods=['POST'])
def index2():
    if request.form.get('team'):
        add_winner_to_list(request.form.get('team'))
    elif request.form.get('manageTeams'):
        if request.form.get('player') and request.form.get('manageTeams') == "addPlayer" and len(rounds) == 0:
            add_to_registered_teams(request.form.get('player'))
        elif request.form.get('manageTeams') == "blockAddPlayer":
            start_game()
    elif request.form.get('member'):
        # print(request.form.get('memberName'))
        # print(request.form.get('memberTeam'))
        add_member_to_registered_teams(request.form.get('memberName'), request.form.get('memberTeam'))
        # Add team member
    elif request.form.get('reset'):
        reset_all()

    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description,
                           registered_teams=registered_teams, rounds=rounds, current_round=current_round, winner=winner, selected_team=selected_team)
