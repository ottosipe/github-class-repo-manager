import os
import sys
import json

from github import Github
from flask import *
from pymongo import MongoClient

from auth import *

app = Flask(__name__)
app.register_blueprint(auth)
app.debug = True
app.secret_key = os.environ['APP_SECRET']
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

mongo = MongoClient('paulo.mongohq.com', 10060)
mongo.eecs485_users.authenticate(os.environ['DB_USER'], os.environ['DB_PASS'])
users_db = mongo.eecs485_users.users
teams_db = mongo.eecs485_users.teams

users_db.ensure_index("uniqname", unique=True, dropDups=True);
teams_db.ensure_index("id", unique=True, dropDups=True);

MAX_TEAM = 3

@app.route('/')
def main():
    return render_template("index.jade")

#API to ADD/EDIT User
@app.route('/user', methods=["GET","POST"])
@auth_check
def user(github):
    
    user_info = getGHcreds(github)
    user = users_db.find_one({ "github": user_info["github"] })

    if request.method == "GET":


        if user:
            user_info["uniqname"] = user["uniqname"]
            user_info["team_id"] = user["team_id"]

        return render_template('user.jade', **user_info)

    else: #POST
        user_info["uniqname"] = request.json["uniqname"]
        team_id = user_info["team_id"] = request.json["team_id"]

        team = teams_db.find_one({"id":team_id})

        #check if team exists
        if (team_id != "") and (not team):
            return json.dumps({"error":"Invalid Team Id!"})

        # check if team is full
        if team and team["size"] >= MAX_TEAM and user["team_id"] != team_id:
            return json.dumps({"error": "Team is Full! Maximum Team Size is " + str(MAX_TEAM)})

        # save the user
        users_db.update({ "github":user_info["github"] }, user_info, upsert= True);

        # increment user count for team
        if team:
            team["size"] += 1
            teams_db.update({ "id": team_id }, team)

        return json.dumps({"success" : 'ok'})


#API to ADD/EDIT team
@app.route('/team/<id>', methods=["GET","POST"])
@auth_check
def team(github, id):

    user = getGHcreds(github)

    team = teams_db.find_one({"id":id})

    #view UI for team
    if request.method == "GET":
        # team id doesnt exist in DB
        if not team: team = {}

        # team is valid
        team["members"] = []
        seenUser = False
        for member in users_db.find({ "team_id":id }):
            team["members"].append(member)
            if member["github"] == user["github"]: 
                seenUser = True

        # prevent others from changing group
        if not seenUser: 
            team = {}
        
        return render_template('team.jade', **team)

    else: #POST

        team["name"] = request.json["name"]
        teams_db.update({"id": id}, team);
        return json.dumps({"success" : 'ok'})


@app.route('/key', methods=["POST"])
@auth_check
def key(github):

    user = getGHcreds(github)
    key = request.form["key"];

    team = {
        "id": key,
        "name": "",
        "creator": user["github"],
        "size": 0
    }
    # todo: check that user is not in a team already!
    teams_db.insert(team);

    return "done"
