from flask import Flask

app = Flask(__name__)

@app.route('/')
def get():
    return 'Hello, World!'



from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )
    conn.commit()
    conn.close()

    return "User registered!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5000)

