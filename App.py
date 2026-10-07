from flask import Flask, jsonify, request
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def home():
    return jsonify({"message": "TaskFlow API is running"})


@app.route("/users", methods=["GET"])
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    return jsonify(users)


@app.route("/users", methods=["Post"])
def create_user():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
        (data["name"], data["email"])
        )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "name": data["name"], "email": data["email"]}), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"id": row[0], "name": row[1], "email": row[2]})

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s;", (data["name"], data["email"], user_id)
    )
    conn.commit()
    updated = cur.rowcount
    cur.close()
    conn.close()

    if updated == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"id": user_id, "name": data["name"], "email": data["email"]})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()
    deleted = cur.rowcount
    cur.close()
    conn.close()

    if deleted == 0:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = 5000)