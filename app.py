import os
import sys
import json
import requests

from github import Github
from flask import *
from pymongo import MongoClient

app = Flask(__name__)
app.debug = True
app.secret_key = 'YEah,PrEtTY_SECreT.'
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

CLIENT_ID = "685178b367d43cf4c7f1"
CLIENT_SECRET = "c580f07164fd6f316fb5154a16c13b431536b735"
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
REDIRECT_URI = "http://localhost/"

mongo = MongoClient('paulo.mongohq.com', 10060)
mongo.eecs485_users.authenticate('eecs485', 'blue13mjmo')
users_db = mongo.eecs485_users.users
teams_db = mongo.eecs485_users.teams

users_db.ensure_index("uniqname", unique=True, dropDups=True);
teams_db.ensure_index("id", unique=True, dropDups=True);

@app.route('/')
def main(): 
    oauth = session.get('oauth_token',"")
    if (oauth == ""): return redirect(url_for("login"))

    g = Github(oauth)
    org = g.get_organization("EECS485")

    out = ""
    for repo in org.get_repos():
        out += repo.name + " "

    return "logged in with token " + oauth + "\n" + out


@app.route('/users', methods=["GET","POST"])
def addUser():
    #request.args.get("groupHash", "")
    user_info = {
        "uniqname": request.args.get("uniqname", ""),
        "github": request.args.get("github", "")
    }

    users_db.insert(user_info);

    return "done"




"""
Login and OAuth Routes:

"""

@app.route('/login')
def login():
    return redirect(GITHUB_AUTH_URL+
            "?client_id="+ CLIENT_ID +
            "&scope=repo")

@app.route('/auth')
def auth(): 

    code = request.args.get("code", "")
    if (code == ""): return "auth fail"

    payload = { "client_id": CLIENT_ID, 
                "client_secret": CLIENT_SECRET,
                "code": code }

    headers = {'accept': 'application/json'}

    res = requests.get(GITHUB_TOKEN_URL, params=payload, headers=headers)

    session['oauth_token'] = res.json()['access_token']

    return redirect(url_for("main"))
