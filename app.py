from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("diary_entries.json")


def load_entries() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_entries(entries: list[dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2, ensure_ascii=False)


def add_entry() -> None:
    print("\nWrite your diary entry. Press Enter on an empty line to finish:\n")
    lines: list[str] = []

    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    if not lines:
        print("No text entered. Entry not saved.\n")
        return

    text = "\n".join(lines)
    entry = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
    }

    entries = load_entries()
    entries.append(entry)
    save_entries(entries)
    print("Entry saved successfully.\n")


def view_entries() -> None:
    entries = load_entries()
    if not entries:
        print("\nNo diary entries yet.\n")
        return

    print(f"\nYou have {len(entries)} entries:\n")
    for index, entry in enumerate(entries, start=1):
        print("-" * 50)
        print(f"Entry {index} | {entry['created_at']}")
        print("-" * 50)
        print(entry["text"])
        print()


def main() -> None:
    while True:
        print("==== Digital Diary ====")
        print("1) New Entry")
        print("2) View Entries")
        print("3) Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            add_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            print("Goodbye. Your diary is saved locally.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.\n")


if __name__ == "__main__":
    main()
