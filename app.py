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
app.secret_key = 'YEah,PrEtTY_SECreT.'
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

mongo = MongoClient('paulo.mongohq.com', 10060)
mongo.eecs485_users.authenticate('eecs485', 'blue13mjmo')
users_db = mongo.eecs485_users.users
teams_db = mongo.eecs485_users.teams

users_db.ensure_index("uniqname", unique=True, dropDups=True);
teams_db.ensure_index("team_id", unique=True, dropDups=True);


@app.route('/')
def main():
    return render_template("index.jade")

#API to ADD/EDIT User
@app.route('/user', methods=["GET","POST"])
@auth_check
def user(github):
    
    user_info = getGHcreds(github)
    
    if request.method == "GET":

        user = users_db.find_one({ "github": user_info["github"] })
        if user_info:
            user_info["uniqname"] = user["uniqname"]
            user_info["team_id"] = user["team_id"]

        return render_template('user.jade', **user_info)

    else:
        user_info["uniqname"] = request.json["uniqname"]
        user_info["team_id"] = request.json["team_id"]

        users_db.update({ "github":user_info["github"] }, user_info, upsert= True);

        return json.dumps({"status" : 'done'})


#API to ADD/EDIT team
@app.route('/team/<id>', methods=["GET","POST"])
@auth_check
def team(github, id):

    user = getGHcreds(github)

    team = teams_db.find_one({"id":id})

    #view UI for team
    if request.method == "GET":
        # lookup id in teams
        # if it doesnt exist throw error
        # else show teammates and allow edits
        if not team: team = {}

        team["members"] = []
        for member in users_db.find({ "team_id":id }):
            team["members"].append(member)

        return render_template('team.jade', **team)

    #API to ADD/EDIT team
    else:

        #teams_db.update({"team_id":user_info["team_id"]}, team_info);
        return "Group Saved"


@app.route('/key', methods=["POST"])
@auth_check
def key(github):

    user = getGHcreds(github)
    key = request.form["key"];

    team = {
        "id": key,
        "name": "",
        "creator": user["github"]
    }
    # todo: check that user is not in a team already!
    teams_db.insert(team);

    return "done"
