# Digital Diary (Python Web App)

A mini-project digital diary website built with Python and Flask.
It includes user authentication, a real SQLite database, and owner-only diary management.

## Features

- Register and login system with hashed passwords
- Personal diary dashboard for each user
- Create, edit, and delete entries
- Owner-only access control (users can only modify their own entries)
- Real database storage using SQLite (`diary.db`)
- Browser opens automatically when app starts

## Tech Stack

- Python 3
- Flask
- SQLite (built-in with Python)

## Steps to Run

1. Open terminal in this folder.
2. Install dependencies:

```bash
py -m pip install -r requirements.txt
```

3. Run the app:

```bash
py app.py
```

4. App opens in browser automatically. If needed, visit:

```text
http://127.0.0.1:5000
```

## Suggested GitHub Collaboration Strategy

- Do not code directly on `main`
- Create feature branches:
  - `feature-auth`
  - `feature-diary-crud`
  - `feature-ui-docs`
- Raise pull requests and review each other before merge

## Team Member Contributions

Update this section with your real names before submission:

| Team Member | Branch | Contribution |
| --- | --- | --- |
| Member 1 | `feature-auth` | Login/register, session management |
| Member 2 | `feature-diary-crud` | Add/view/edit/delete diary entries |
| Member 3 | `feature-ui-docs` | UI polish, README, testing, video |

## Demo Video

Add your project demo link here (Google Drive / YouTube):

`<PASTE_VIDEO_LINK_HERE>`

## GitHub Repository Link

Add your final repository URL here:

`<PASTE_GITHUB_REPO_LINK_HERE>`
