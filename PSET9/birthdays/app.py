import os
from cs50 import SQL
from flask import Flask, render_template, request
#configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Add the user's entry into the database
        m = ""
        inputname = request.form.get("name")
        inputmonth = request.form.get("month")
        inputday = request.form.get("day")
        if not inputname:
            m = "You didn't enter a name!"
        elif not inputday:
            m = "Birthday is missing from your input"
        elif not inputmonth:
            m = "You didn't enter a birth month"
        else:
            db.execute(
                "INSERT INTO birthday (name, month, day) VALUES(?, ?, ?)",
                inputname,
                inputmonth,
                inputday,
            )
            birthdays = db.execute("SELECT * FROM birthdays")
            return render_template("index.html", m=m, birthdays=birthdays)

    # Display the entries in the database on index.html
    birthdays = db.execute("SELECT * FROM birthdays")
    return render_template("index.html", birthdays=birthdays)
