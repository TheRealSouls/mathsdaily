from cs50 import SQL
from flask import Flask, render_template, session, request, redirect, make_response, flash, get_flashed_messages
from flask_session import Session
from functools import wraps
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['TEMPLATES_AUTO_RELOAD'] = True
Session(app)

db = SQL("sqlite:///dailymaths.db")

def nocache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = "0"
        response.headers["Pragma"] = "no-cache"
        return response
    return no_cache_view

@app.route("/contact")
def contact():
    return render_template("contact.html", title="DailyMaths.ie - Contact")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/leaderboard")
def leaderboard():
    # TODO
    return render_template("leaderboard.html", title="DailyMaths.ie - Leaderboard") 

@app.route("/login", methods=["GET", "POST"])
@nocache
def login():
    if request.method == "POST":
        # TODO
        pass
    else:
        return render_template("login.html", title="DailyMaths.ie - Login")

@app.route("/register", methods=["GET", "POST"])
@nocache
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

        if not username:
            flash("Username is required", "error")
        if not password:
            flash("Password is required", "error")
        if not email:
            flash("Email is required", "error")
        elif EMAIL_REGEX.match(email) is None:
            flash("Invalid email format", "error")
        if password != confirm_password:
            flash("Passwords do not match", "error")

        # check if username or email exists
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if user:
            flash("Username already taken", "error")
        
        user_email = db.execute("SELECT * FROM users WHERE email = ?", email)
        if user_email:
            flash("Email already registered", "error")
        
        # If any errors, redisplay form.
        if get_flashed_messages(category_filter=["error"]):
            return render_template("register.html", errors=errors, title="DailyMaths.ie - Register")

        db.execute(
            "INSERT INTO users (username, password_hash, score, email) VALUES (?, ?, ?, ?)",
              username, generate_password_hash(password), 0, email
        )
        return redirect("/homepage")

    # GET request
    return render_template("register.html", title="DailyMaths.ie - Register", errors={})