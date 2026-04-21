from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)
DATA_FILE = Path("diary_entries.json")


def load_entries() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_entries(entries: list[dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2, ensure_ascii=False)


@app.get("/")
def home() -> str:
    entries = load_entries()
    # Newest entries shown first for a better diary view.
    return render_template("index.html", entries=reversed(entries))


@app.post("/add")
def add_entry() -> str:
    text = request.form.get("entry_text", "").strip()
    if text:
        entries = load_entries()
        entries.append(
            {
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "text": text,
            }
        )
        save_entries(entries)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
