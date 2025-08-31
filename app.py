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

@app.route("/challenge/<int:challenge_id>")
def challenge(challenge_id):

    if session.get("user_id") is None:
        session.clear()
        return redirect("/")
    
    submission = True
    
    solved = db.execute(
        "SELECT * FROM solved_problems WHERE user_id = ? AND problem_id = ?",
        session["user_id"], challenge_id
    )

    if solved:
        submission = False

    problem = db.execute("SELECT * FROM math_problems WHERE problem_id = ?", challenge_id)
    # TODO: WHERE date_added = ?, but for now I'm just testing

    if not problem:
        return "No challenge added today", 404

    return render_template("auth/challenge.html", 
                           challenge=problem[0],
                           submission=submission
                           )

@app.route("/homepage")
def homepage():
    if session.get("user_id") is None:
        session.clear()
        return redirect("/")
    
    challenges = db.execute("SELECT * FROM math_problems")
    # TODO: adjust query for only TODAY.
    
    data = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
    username = data[0]["username"] if data else None
    solved = data[0]["solved"] if data else 0
    accuracy = data[0]["accuracy"] if data else 0

    messages = get_flashed_messages(with_categories=True)

    return render_template("auth/homepage.html",
                            data=data, 
                            challenges=challenges,
                            messages=messages
                        )

@app.route("/")
def index():
    if session.get("user_id"):
        return redirect("/homepage")

    challenge = db.execute("SELECT * FROM math_problems")
    return render_template(
        "dashboard/index.html",
        challenge=challenge
        )

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
    if session.get("user_id"):
        return render_template("auth/leaderboard.html", title="DailyMaths.ie - Leaderboard")

    return render_template("dashboard/leaderboard.html", title="DailyMaths.ie - Leaderboard") 

@app.route("/login", methods=["GET", "POST"])
@nocache
def login():

    if session.get("user_id"):
        return redirect("/homepage")

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
@nocache
def register():
    if request.method == "POST":

        if session.get("user_id"):
            return redirect("/homepage")

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

@app.route("/submit/<int:challenge_id>", methods=["POST"])
def submit_challenge(challenge_id):
    if session.get("user_id") is None:
        flash("⚠️ Please log in first to attempt the challenge.", "error")
        return redirect("/login")
    
    user_id = session["user_id"]
    option = request.form.get("answer")

    solved = db.execute(
        "SELECT * FROM solved_problems WHERE user_id = ? AND problem_id = ?",
        user_id, challenge_id
    )

    if solved:
        flash("⚠️ You cannot submit a challenge twice. Nice try!", "error")
        return redirect("/homepage")

    if not option or not option.isdigit():
        flash("⚠️ Invalid answer submission.", "error")
        return redirect(f"/challenge/{challenge_id}")
    
    option = int(option)

    problem = db.execute("SELECT * FROM math_problems WHERE problem_id = ?", challenge_id)
    if not problem:
        flash("⚠️ Challenge not found.", "error")
        return redirect("/homepage")
    
    problem = problem[0]
    correct_option = problem["correct_option"]

    is_correct = 1 if option == correct_option else 0

    db.execute(
        "INSERT INTO solved_problems (user_id, problem_id, correct) VALUES (?, ?, ?)",
        user_id, challenge_id, is_correct
    )

    user = db.execute("SELECT * FROM users WHERE user_id = ?", user_id)[0]

    solved = user["solved"] or 0
    accuracy = user["accuracy"] or 0.0
    score = user["score"] or 0

    new_solved = solved + 1
    new_accuracy = ((accuracy * solved) + is_correct) / new_solved
    new_score = score + (problem["points"] if is_correct else 0)

    db.execute(
        "UPDATE users SET solved = ?, accuracy = ?, score = ? WHERE user_id = ?",
        new_solved, new_accuracy, new_score, user_id
    )

    if is_correct:
        flash("✅ Correct! Well done.", "success")
    else:
        flash("❌ Incorrect. Try again tomorrow!", "error")
    
    return redirect("/homepage")

    