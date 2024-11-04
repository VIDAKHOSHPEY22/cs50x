from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SECRET_KEY"] = "my_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


# Define the usd filter
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


# Add the usd filter to the Jinja environment
app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Ensure tables exist in the database
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    );
""")

db.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
""")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    total = cash
    for stock in portfolio:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["total_value"] = stock["total_shares"] * quote["price"]
        total += stock["total_value"]
    return render_template("index.html", portfolio=portfolio, cash=cash, total=total, usd=usd)

# Add your other routes here...


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username and password are provided
        if not username or not password or not confirmation:
            return apology("Username and password are required!")

        # Ensure password and confirmation match
        if password != confirmation:
            return apology("Passwords do not match!")

        # Further validation logic for username and password can be added here

        # Check if username already exists
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return apology("Username already exists!")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert user into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        flash("Registration successful! Please log in.")
        return redirect("/login")
    else:
        return render_template("register.html")

        # login


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password are provided
        if not username or not password:
            return apology("Username and password are required!")

        # Query database for username
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check if username exists and password is correct
        if not user or not check_password_hash(user[0]["hash"], password):
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        flash("Logged in successfully!")
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("You must enter a symbol")
        if not shares or shares < 1:
            return apology("Shares must be a positive integer")

        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol")

        user_id = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
        cash = user["cash"]
        total_cost = quote["price"] * shares

        if cash < total_cost:
            return apology("Insufficient funds")

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, datetime('now'))",
                   user_id, symbol, shares, quote["price"])

        # Update user's cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_cost, user_id)

        flash("Purchase successful!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show transaction history"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("You must select a symbol")

        if not shares or int(shares) < 1:
            return apology("Shares must be a positive integer")

        # Proceed with the rest of your code to handle the sell transaction
        # Make sure to validate other form fields and perform necessary database operations
    else:
        user_id = session["user_id"]
        symbols = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", user_id)
        return render_template("sell.html", symbols=symbols)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("You must enter a symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol")
        stock["price"] = usd(stock["price"])
        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")
        # deposit


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        # Get form data
        password = request.form.get("password")
        amount = request.form.get("sum")

        # Validate password and amount
        if not password:
            return apology("Password is required")
        if not amount or int(amount) < 10:
            return apology("Amount must be at least $10")

        # Query database for user's cash balance
        user_id = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]

        # Confirm password
        if not check_password_hash(user["hash"], password):
            return apology("Invalid password")

        # Update user's cash balance
        new_cash_balance = user["cash"] + int(amount)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, user_id)

        flash("Deposit successful!")
        return redirect("/")
    else:
        return render_template("deposit.html")


@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    if request.method == "POST":
        password = request.form.get("password")
        amount = request.form.get("sum")

        # Check if password is confirmed
        if not password:
            return apology("Confirm password is required!")

        # Check if amount is provided and valid
        if not amount or int(amount) < 10:
            return apology("Amount must be at least $10")

        # Further processing logic goes here

        flash("Withdrawal successful!")
        return redirect("/")
    else:
        return render_template("withdraw.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    # Forget user_id
    session.clear()
    flash("Logged out successfully!")
    return redirect("/")
