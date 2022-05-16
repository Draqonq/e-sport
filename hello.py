from contextlib import nullcontext
from multiprocessing.dummy import Array
from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import random
import math

app = Flask(__name__)


tournamentName = "Chess Master"
tournamentDescription = "W turnieju mogą wziąć udział studenci informatyki stosowanej oraz teleinformatyki. Liczymy na zwycięztwo informatyków!"
round1 = 6
round2 = 3
round1team = {"wolo", "bolo", "zolo", "trolo"}
round2team = {"br11"}

app.config['MONGO_URI'] = 'mongodb+srv://Piorob:Robpio@cluster0.cftar.mongodb.net/serwisy?retryWrites=true&w=majority'
mongo = PyMongo(app)

teams = mongo.db.teams

class Tournament:
    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

class Round:
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
        


#create fight
#if(len(tournament1.teams) % 2 == 0):
    #for i in (len(tournament1.teams)/2):
        #Round("round"+i)
#else:
    #for i in ((len(tournament1.teams)+1)/2):
        #print("x")

#tournament name + registered teams
tournament_name = "Chess Master"
tournament_description = "W turnieju mogą wziąć udział studenci informatyki stosowanej oraz teleinformatyki. Liczymy na zwycięztwo informatyków!"
registered_teams = ["Alakonda", "Mojowojo", "TeamXD", "Bałkan", "WODOGRZOM"]
tournament = Tournament(tournament_name, registered_teams)
#round
round0 = Round("Round 0", tournament.teams)
round1 = Round("Round 1", [])
round = [round0, round1]
#fight
round[0].teams = random_fight(round[0])


@app.route('/')
def index():
    saved_todos = teams.find()
    #teams.insert_one({'teams' : 'xddd'})
    return render_template('index.html', tournament_name=tournament_name, tournament_description=tournament_description, round=round)