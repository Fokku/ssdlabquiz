import re
import pymysql
import requests

BASE = "http://localhost:5000"
DB = dict(host="127.0.0.1", port=3306, user="admin",
          password="2403201@sit.singaporetech.edu.sg", database="quizdb")

session = requests.Session()


def logged(username):
    with pymysql.connect(**DB) as conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM `2403201` WHERE username=%s", (username,))
        return cur.fetchone()[0]


# Forms are CSRF-protected: fetch the page holding the form to obtain the
# token (and session cookie), then submit it alongside the credentials.
def form_post(form_page, action, data, **kwargs):
    token = re.search(r'name="csrf_token" value="([^"]+)"',
                      session.get(BASE + form_page).text).group(1)
    return session.post(BASE + action, data={**data, "csrf_token": token}, **kwargs)


# Home page serves the login form with username + password fields (req 1)
home = session.get(BASE + "/").text
assert "username" in home and "password" in home

# Account creation page is reachable (req 6)
assert session.get(BASE + "/register").status_code == 200

# Strong unique password -> Welcome shows the password and the user is logged (req 8, 9)
strong = "Integration-Pass-1!"
r = form_post("/register", "/register", {"username": "int_ok", "password": strong})
assert r.status_code == 200 and "Welcome" in r.text and strong in r.text
assert logged("int_ok") == 1

# Common password from the database -> stay at home, not logged (req 5, 7)
r = form_post("/register", "/register",
              {"username": "int_common", "password": "1q2w3e4r5t6y"},
              allow_redirects=False)
assert r.status_code == 302 and logged("int_common") == 0

# Password too short -> stay at home (req 3, 7)
r = form_post("/", "/login", {"username": "int_ok", "password": "short"},
              allow_redirects=False)
assert r.status_code == 302

# POST without a CSRF token is rejected (SonarQube python:S4502 fix)
r = requests.post(BASE + "/login",
                  data={"username": "int_ok", "password": strong})
assert r.status_code == 400

print("Integration tests passed")
