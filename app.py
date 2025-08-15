from cs50 import SQL
from flask import Flask, render_template, session, request
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['TEMPLATES_AUTO_RELOAD'] = True
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="DailyMaths.ie - Contact")

@app.route("/leaderboard")
def leaderboard():
    # TODO
    return render_template("leaderboard.html", title="DailyMaths.ie - Leaderboard") 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass
    else:
        return render_template("login.html", title="DailyMaths.ie - Login")

