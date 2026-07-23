import pymysql
import requests

BASE = "http://localhost:5000"
DB = dict(host="127.0.0.1", port=3306, user="admin",
          password="2403201@sit.singaporetech.edu.sg", database="quizdb")


def logged(username):
    with pymysql.connect(**DB) as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM `2403201` WHERE username=%s", (username,))
        return cur.fetchone()[0]


# Home page serves the login form with username + password fields (req 1)
home = requests.get(BASE + "/").text
assert "username" in home and "password" in home

# Account creation page is reachable (req 6)
assert requests.get(BASE + "/register").status_code == 200

# Strong unique password -> Welcome shows the password and the user is logged (req 8, 9)
strong = "Integration-Pass-1!"
r = requests.post(BASE + "/register", data={"username": "int_ok", "password": strong})
assert r.status_code == 200 and "Welcome" in r.text and strong in r.text
assert logged("int_ok") == 1

# Common password from the database -> stay at home, not logged (req 5, 7)
r = requests.post(BASE + "/register",
                  data={"username": "int_common", "password": "1q2w3e4r5t6y"},
                  allow_redirects=False)
assert r.status_code == 302 and logged("int_common") == 0

# Password too short -> stay at home (req 3, 7)
r = requests.post(BASE + "/login", data={"username": "int_ok", "password": "short"},
                  allow_redirects=False)
assert r.status_code == 302

print("Integration tests passed")
