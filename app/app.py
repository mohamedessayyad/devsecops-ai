import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Fausse clé AWS laissée exprès pour que gitleaks la détecte
AWS_ACCESS_KEY_ID = "AKIAZ3MSJV4WWNKWW5FG"


def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.execute("DELETE FROM users")
    conn.execute("INSERT INTO users (name, email) VALUES ('alice', 'alice@test.ma')")
    conn.execute("INSERT INTO users (name, email) VALUES ('bob', 'bob@test.ma')")
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "DevSecOps demo app - essaie /user?name=alice"


@app.route("/user")
def user():
    name = request.args.get("name", "")
    conn = sqlite3.connect("users.db")
    # Injection SQL volontaire
    query = "SELECT name, email FROM users WHERE name = '" + name + "'"
    rows = conn.execute(query).fetchall()
    conn.close()
    return {"query": query, "result": rows}


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
