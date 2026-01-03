from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table
conn = get_db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
conn.close()

@app.route("/")
def register():
    return render_template("register.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO registrations (name, email) VALUES (?, ?)",
        (name, email)
    )
    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/admin")
def admin():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM registrations").fetchall()
    count = len(users)
    conn.close()

    return render_template("admin.html", users=users, count=count)

if __name__ == "__main__":
    app.run(debug=True)
