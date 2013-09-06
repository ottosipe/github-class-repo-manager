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
teams_db.ensure_index("group_id", unique=True, dropDups=True);



@app.route('/')
def main():
    return "welcome"

#API to ADD/EDIT User
@app.route('/user', methods=["GET","POST"])
@auth_check
def user(github):
    
    user_info = getGHcreds(github)
    
    if request.method == "GET":

        user = users_db.find_one({ "github": user_info["github"] })
        if user_info:
            user_info["uniqname"] = user["uniqname"]
            user_info["group_id"] = user["group_id"]

        return render_template('index.jade', **user_info)

    else:

        user_info["uniqname"] = request.json["uniqname"]
        user_info["group_id"] = request.json["group_id"]

        users_db.update({"github":user_info["github"]}, user_info, upsert= True);

        return "done"


#API to ADD/EDIT group
@app.route('/group/<id>', methods=["GET","POST"])
@auth_check
def group(github, id):

    obj = getGHcreds(github)
    #view UI for group
    if request.method == "GET":
        # lookup id in teams
        # if it doesnt exist throw error
        # else show teammates and allow edits
        return render_template('group.jade')

    #API to ADD/EDIT group

    #teams_db.update({"group_id":user_info["group_id"]}, team_info, upsert= True);
    return "Group Saved"

