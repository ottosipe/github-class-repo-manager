from flask import *
from functools import wraps
import requests
from github import Github

CLIENT_ID = "685178b367d43cf4c7f1"
CLIENT_SECRET = "c580f07164fd6f316fb5154a16c13b431536b735"
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
REDIRECT_URI = "http://localhost/"

def getGHcreds(g):
    user = g.get_user()
    return {
        "name": user.name,
        "github": user.login,
        "pic": user.avatar_url,
        "email": user.email,
        "uniqname": "",
        "group_id": ""
    }

def auth_check(f):
    # OAuth decorator - forces the use to login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        oauth = session.get('oauth_token',"")
        if oauth == "": return redirect("/login")

        #try:
        g = Github(oauth)
            #user = g.get_user().login
        #except:
            #return redirect("/login")

        return f(g, *args, **kwargs)
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
    return "done"

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

    print res.text
    session['oauth_token'] = res.json()['access_token']

    return redirect("/user")