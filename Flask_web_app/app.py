from flask import Flask, render_template, request, redirect
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users")
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("users.html", users=users)

@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/users")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
