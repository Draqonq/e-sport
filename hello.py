from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://Piorob:Robpio@cluster0.cftar.mongodb.net/serwisy?retryWrites=true&w=majority'
mongo = PyMongo(app)

teams = mongo.db.teams

@app.route('/')
def index():
    saved_todos = teams.find()
    teams.insert_one({'teams' : 'xddd'})
    return render_template('index.html')

# app = Flask(__name__)

# tournamentName = "Chess Master"
# tournamentDescription = "W turnieju mogą wziąć udział studenci informatyki stosowanej oraz teleinformatyki. Liczymy na zwycięztwo informatyków!"

# @app.route('/')
# def main():
#     return render_template('index.html', TName=tournamentName, TDesc=tournamentDescription)

# @app.route('/test')
# def test():
#     return 'Strona testowa'

# if __name__ == '__main__':
#     app.run(debug=True)

