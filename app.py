from __future__ import annotations

import hashlib
import os
import sqlite3
import threading
import webbrowser
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DATABASE_FILE = Path("diary.db")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        connection = sqlite3.connect(DATABASE_FILE)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


@app.teardown_appcontext
def close_db(_: object) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    db.commit()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def current_user() -> sqlite3.Row | None:
    user_id = session.get("user_id")
    if user_id is None:
        return None
    db = get_db()
    return db.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()


@app.before_request
def ensure_db() -> None:
    init_db()


@app.get("/")
def home() -> str:
    user = current_user()
    if user is None:
        return redirect(url_for("login"))
    db = get_db()
    entries = db.execute(
        """
        SELECT id, title, content, created_at, updated_at
        FROM entries
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user["id"],),
    ).fetchall()
    return render_template("index.html", user=user, entries=entries)


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("register"))

        db = get_db()
        existing_user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            flash("Username already exists. Please choose another one.", "error")
            return redirect(url_for("register"))

        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password)),
        )
        db.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        db = get_db()
        user = db.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if user is None or user["password_hash"] != hash_password(password):
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))

        session["user_id"] = user["id"]
        flash("Logged in successfully.", "success")
        return redirect(url_for("home"))
    return render_template("login.html")


@app.post("/logout")
def logout() -> str:
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.post("/add")
def add_entry() -> str:
    user = current_user()
    if user is None:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if not title or not content:
        flash("Title and content are required.", "error")
        return redirect(url_for("home"))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    db.execute(
        """
        INSERT INTO entries (user_id, title, content, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user["id"], title, content, now, now),
    )
    db.commit()
    flash("Entry added.", "success")
    return redirect(url_for("home"))


@app.post("/edit/<int:entry_id>")
def edit_entry(entry_id: int) -> str:
    user = current_user()
    if user is None:
        return redirect(url_for("login"))

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if not title or not content:
        flash("Title and content are required for editing.", "error")
        return redirect(url_for("home"))

    db = get_db()
    updated_rows = db.execute(
        """
        UPDATE entries
        SET title = ?, content = ?, updated_at = ?
        WHERE id = ? AND user_id = ?
        """,
        (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), entry_id, user["id"]),
    ).rowcount
    db.commit()
    if updated_rows == 0:
        flash("Entry not found or permission denied.", "error")
    else:
        flash("Entry updated.", "success")
    return redirect(url_for("home"))


@app.post("/delete/<int:entry_id>")
def delete_entry(entry_id: int) -> str:
    user = current_user()
    if user is None:
        return redirect(url_for("login"))

    db = get_db()
    deleted_rows = db.execute(
        "DELETE FROM entries WHERE id = ? AND user_id = ?",
        (entry_id, user["id"]),
    ).rowcount
    db.commit()
    if deleted_rows == 0:
        flash("Entry not found or permission denied.", "error")
    else:
        flash("Entry deleted.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True)
