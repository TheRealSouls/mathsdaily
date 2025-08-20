from cs50 import SQL
from flask import Flask, render_template, session, request, redirect, make_response, flash, get_flashed_messages
from flask_session import Session
from functools import wraps
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-for-local")

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
    return render_template("dashboard/contact.html", title="DailyMaths.ie - Contact")

@app.route("/homepage")
def homepage():
    # TODO: Finish
    if session.get("user_id") is None:
        session.clear()
        return redirect("/")
    
    rows = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])
    username = rows[0]["username"] if rows else None

    return render_template("auth/homepage.html", username=username)

@app.route("/")
def index():
    if session.get("user_id"):
        return redirect("/homepage")
    return render_template("dashboard/index.html")

@app.route("/api/leaderboard")
def leaderboard_api():
    limit = request.args.get("limit", 10, type=int)

    rows = db.execute(
        "SELECT username, score, solved, accuracy FROM users ORDER BY score DESC LIMIT ?",
        limit,
    )

    return rows

@app.route("/leaderboard")
def leaderboard():
    return render_template("dashboard/leaderboard.html", title="DailyMaths.ie - Leaderboard") 

@app.route("/login", methods=["GET", "POST"])
@nocache
def login():

    session.clear()

    if request.method == "POST":
        username_email = request.form.get("username-email")
        password = request.form.get("password")

        errors = []

        if not username_email:
            errors.append(("⚠️ Username or email is required", "error"))
        
        if not password:
            errors.append(("⚠️ Password is required", "error"))

        if not errors:
            rows = db.execute(
                "SELECT * FROM users WHERE username = ? OR email = ?", username_email, username_email
            )

            # TODO: remember me functionality

            if len(rows) != 1 or not check_password_hash(
                rows[0]["password_hash"], password
            ):
                errors.append(("⚠️ Invalid username and/or password", "error"))
        
        if errors:
            return render_template("dashboard/login.html", title="DailyMaths.ie - Login", errors=errors)

        session["user_id"] = rows[0]["user_id"]
        
        return redirect("/homepage")
    
    # GET request
    return render_template("dashboard/login.html", title="DailyMaths.ie - Login", errors=[])

@app.route("/register", methods=["GET", "POST"])
@nocache
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        errors = []
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

        if not username:
            errors.append(("⚠️ Username is required", "error"))
        
        if not password:
            errors.append(("⚠️ Password is required", "error"))
        
        if not email:
            errors.append(("⚠️ Email is required", "error"))
        
        elif EMAIL_REGEX.match(email) is None:
            errors.append(("⚠️ Invalid email format", "error"))
        
        if password != confirm_password:
            errors.append(("⚠️ Passwords do not match", "error"))

        # check if username or email exists
        if username and db.execute("SELECT * FROM users WHERE username = ?", username):
            errors.append(("⚠️ Username already taken", "error"))
        
        if email and db.execute("SELECT * FROM users WHERE email = ?", email):
            errors.append(("⚠️ Email already registered", "error"))
        
        if errors:
            return render_template("dashboard/register.html", title="DailyMaths.ie - Register", errors=errors)
        
        try:
            db.execute(
                "INSERT INTO users (username, password_hash, score, email) VALUES (?, ?, ?, ?)",
                username, generate_password_hash(password), 0, email
            )
        except Exception as exc:
            # catch integrity / other DB errors and show a user-friendly message
            errors.append(("⚠️ Account could not be created due to an unknown error. Please report this to the staff!", "error"))
            # optionally log the exception server-side
            app.logger.exception("Register DB error")
            return render_template("register.html", title="DailyMaths.ie - Register", errors=errors)


        # TODO: remember me functionality

        flash("✅ Account created! Please log in.", "success")
        return redirect("/login")

    # GET request
    return render_template("dashboard/register.html", title="DailyMaths.ie - Register")