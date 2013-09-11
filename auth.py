import os
from flask import *
from functools import wraps
import requests
from github import *

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

AUTH_USERS = ["ottosipe","mikecafarella","Jun1113","themattman"]

def getGHcreds(g):
    user = g.get_user()
    return {
        "name": user.name,
        "github": user.login,
        "pic": user.avatar_url,
        "email": user.email,
        "uniqname": "",
        "team_id": ""
    }

def auth_check(f):
    # OAuth decorator - forces the use to login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        oauth = session.get('oauth_token',"")
        if oauth == "": return redirect("/login")

        try:
            g = Github(oauth)
            g.get_user().login
        except BadCredentialsException:
            return redirect("/login")

        return f(g, *args, **kwargs)
    return decorated_function

def admin_check(f):
    # checks if user is admin of page
    @wraps(f)
    def decorated_function(g, *args, **kwargs):

        org = g.get_organization("EECS485")
        login = g.get_user().login

        bad_user = True
        for user in AUTH_USERS:
            if user == login:
                bad_user = False
                break

        if bad_user:
            abort(403)

        return f(org, *args, **kwargs)
    return decorated_function

auth = Blueprint('auth', __name__, template_folder='templates')
"""
Login and OAuth Routes:

"""

@auth.route('/logout')
def logout():
    # get ride of the users token
    # this will force a new login nextime
    session['oauth_token'] = ""
    return redirect("/")

@auth.route('/login')
def login():
    # login endpoint redirects right to github
    session['oauth_token'] = ""
    return redirect(GITHUB_AUTH_URL+
            "?client_id="+ CLIENT_ID +
            "&scope=repo")

@auth.route('/auth')
def oauth(): 
    # get oauth token from GitHub
    # save in session for later!
    code = request.args.get("code", "")
    if (code == ""): return "auth fail"

    payload = { "client_id": CLIENT_ID, 
                "client_secret": CLIENT_SECRET,
                "code": code }

    headers = {'accept': 'application/json'}

    res = requests.get(GITHUB_TOKEN_URL, params=payload, headers=headers)

    session['oauth_token'] = res.json()['access_token']

    return redirect("/user")