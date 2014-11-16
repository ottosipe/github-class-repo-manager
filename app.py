import os
import sys
import json

from github import Github
from flask import *
from pymongo import MongoClient

import utils
from auth import *

app = Flask(__name__)
app.register_blueprint(auth)
app.debug = True
app.secret_key = os.environ['APP_SECRET']
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

db_name = os.environ['DB_NAME']
mongo = MongoClient(os.environ['MONGO_URI'])
users_db = mongo[db_name].users
teams_db = mongo[db_name].teams

users_db.ensure_index("uniqname", unique=True, dropDups=True);
teams_db.ensure_index("id", unique=True, dropDups=True);

MAX_TEAM_MEMBERS = 3

#utils.fixTeamDB(teams_db, users_db)

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
        if team and team["size"] >= MAX_TEAM_MEMBERS and user["team_id"] != team_id:
            return json.dumps({"error": "Team is Full! Maximum Team Size is " + str(MAX_TEAM_MEMBERS)})

        # save the user
        users_db.update({ "github":user_info["github"] }, user_info, upsert= True);

        # increment user count for team 
        if team and (not user or user["team_id"] != team_id):
            # user is new to the team
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

#to quit a team
@app.route('/quit/<id>', methods=["GET","POST"])
@auth_check
def quit(github, id):
    user_info = getGHcreds(github)
    user = users_db.find_one({ "github": user_info["github"] })
    team = teams_db.find_one({"id":id})

    # remeber old team
    old_team = user['team_id']
    # remove them from the team
    user['team_id'] = ""
    users_db.update({ "github":user["github"] }, user);

    # make sure they're on the team
    if team and old_team == id:

        team["size"] -= 1
        # one team member left
        if team["size"] <= 0:
            teams_db.remove({ "id": id })
        # keep the team
        else:
            teams_db.update({ "id": id }, team)
    
    return redirect("/user") 

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

@app.route('/create/<id>') # create a project repo for every group: eg. projectId_groupid
@auth_check
@admin_check
def create_proj(github, id):

    return Response(utils.createProj(teams_db, users_db, github, id), mimetype='text/event-stream')

@app.route('/fix_teams') # fix team counts (you probably wont need this)
@auth_check
@admin_check
def fix_teams(github):

    return Response(utils.fixTeamDB(teams_db, users_db), mimetype='text/event-stream')

@app.route('/csv') # get a csv for all the team members in each group
@auth_check
@admin_check
def csv(github):

    csv = "team_id,user1,user2,user3,count\n"
    for team in teams_db.find({"size": { "$ne": 0 }}):
        csv += team['id'] + ","
        i = MAX_TEAM_MEMBERS
        for user in users_db.find({"team_id":team['id']}):
            csv += user['uniqname'] + ","
            i-=1

        while i:
            csv += ","
            i-=1;

        csv += str(team['size']) + "\n"

    response = Response(csv, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=teams.csv'

    return response

