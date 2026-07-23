from flask import Flask, request, render_template, redirect

app = Flask(__name__)


# Backend check - OWASP Proactive Controls 2024 C7 (Secure Digital Identities),
# Level 1 passwords: at least 12 characters, allow up to 64.
def password_ok(pw):
    return 12 <= len(pw) <= 64


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST"])
def login():
    username, pw = request.form["username"], request.form["password"]
    if password_ok(pw):
        return render_template("welcome.html", username=username, password=pw)
    return redirect("/")
