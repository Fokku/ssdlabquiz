import os
import pymysql
from flask import Flask, request, render_template, redirect

app = Flask(__name__)


def db():
    return pymysql.connect(host=os.environ["DB_HOST"], user=os.environ["DB_USER"],
                           password=os.environ["DB_PASSWORD"], database=os.environ["DB_NAME"])


# Backend check - OWASP Proactive Controls 2024 C7 (Secure Digital Identities),
# Level 1 passwords: at least 12 characters, allow up to 64, and reject
# passwords found in the common/breached password list.
def password_ok(pw):
    if not 12 <= len(pw) <= 64:
        return False
    with db() as conn, conn.cursor() as cur:
        cur.execute("SELECT 1 FROM common_passwords WHERE password = %s", (pw,))
        return cur.fetchone() is None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST"])
def login():
    username, pw = request.form["username"], request.form["password"]
    if password_ok(pw):
        return render_template("welcome.html", username=username, password=pw)
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username, pw = request.form["username"], request.form["password"]
    if not password_ok(pw):
        return redirect("/")
    with db() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO `2403201` (username) VALUES (%s)", (username,))
        conn.commit()
    return render_template("welcome.html", username=username, password=pw)
