# Digital Diary (Python Website)

A simple beginner-friendly diary website built with Python and Flask.

## Features

- Add a new diary entry in a web form
- View all saved entries in the browser
- Entries are saved with date and time
- Data stored locally in `diary_entries.json`

## Run the app

1. Open terminal in this folder.
2. Install dependencies:

```bash
py -m pip install -r requirements.txt
```

3. Start the website:

```bash
py app.py
```

4. Open this in your browser:

```text
http://127.0.0.1:5000
```

## Git + GitHub setup (first time)

Run these commands one by one:

```bash
git init
git add .
git commit -m "Initial digital diary app"
```

Then:

1. Create a new empty repository on GitHub named `digital-diary`.
2. Copy your repo URL from GitHub.
3. Run:

```bash
git remote add origin <YOUR_GITHUB_REPO_URL>
git branch -M main
git push -u origin main
```

After this, your diary code is backed up on GitHub.

## Daily workflow

When you make changes:

```bash
git add .
git commit -m "Describe your change"
git push
```
