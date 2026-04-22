# Food Pantry Notification Project

Desktop app prototype for food pantry communication workflows.

This project uses:

- Python
- Tkinter + Pygubu for the GUI
- SQLite for local data storage
- `bcrypt` for password hashing
- `python-dotenv` for environment-based configuration

## Who This README Is For

- Potential users: See [For Potential Users](#for-potential-users) for what the app currently does, setup steps, and how to run it.
- Developers: See [For Developers](#for-developers) for architecture, workflow, and contribution details.

## Current Project Status

This is an early-stage prototype.

Implemented now:

- GUI navigation between sign-in/sign-up choice, sign-in, sign-up, and dashboard screens
- SQLite schema bootstrap for `roles` and `users`
- Seed data creation (default admin + dummy users)

Not fully implemented yet:

- Real authentication flow (sign-in currently routes to dashboard through a placeholder action)
- Persisted sign-up workflow
- Notification sending, notification logs, user management, and template creation screens

## For Potential Users

### Requirements

- Python 3.12+ recommended
- Tkinter support enabled in your Python installation

### Quick Start (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python rebuild_database.py
python main.py
```

### Optional Configuration

Create a `.env` file in the project root to override defaults:

```env
DATABASE_URL=app/database/database.db
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

If `.env` is not present, built-in defaults from `env.py` are used.

### What You Can Test Right Now

- Launch the app and navigate between sign-in/sign-up views
- Open the dashboard after placeholder login
- Verify role-based dashboard button visibility behavior (`admin`, `member`, `subscriber`)
- Rebuild and inspect seeded data in the local SQLite database

## For Developers

### Tech Stack

- Language: Python
- GUI: Tkinter, Pygubu (`.ui` files)
- DB: SQLite
- Config: `python-dotenv`
- Security utility: `bcrypt`

### Repository Layout

```text
food_pantry_notification_project/
├── main.py
├── rebuild_database.py
├── env.py
├── requirements.txt
app/
├── database/
│   ├── models/
│   └── setup/
├── gui/
│   ├── dashboard/
│   │   ├── models/
│   │   └── ui/
│   ├── logInOut/
│   │   ├── models/
│   │   └── ui/
│   └── utilities/
└── logic/
├── LICENSE
```

### Application Entry Points

- App runtime: `main.py`
- Database bootstrap: `rebuild_database.py`

### Local Development Workflow

1. Create and activate a virtual environment.
2. Install dependencies from `requirements.txt`.
3. (Optional) Create or update `.env` values.
4. Rebuild the database with `python rebuild_database.py`.
5. Start the app with `python main.py`.

### Database Bootstrap Behavior

Running `python rebuild_database.py` currently:

- Locates the database directory
- Creates `database.db` if needed
- Drops and recreates `roles`
- Seeds roles: `admin`, `subscriber`, `member`
- Drops and recreates `users`
- Creates default admin from environment settings
- Inserts dummy users for test data

### Notes On Current Architecture

- `app/gui/GUI.py` is the navigation controller for frame switching.
- `app/gui/logInOut/models/` contains sign-in/sign-up UI model classes.
- `app/gui/dashboard/models/DashBoard.py` currently handles role-based widget visibility and basic dashboard setup.
- `app/logic/` is reserved for business logic extraction as the app grows.
- `app/database/models/Database.py` wraps sqlite connection/cursor/query helpers.

### Suggested Next Development Steps

1. Move login and sign-up actions from placeholder handlers into `app/logic/`.
2. Add validation + DB persistence for sign-up form submissions.
3. Implement actual credential verification in sign-in flow.
4. Add tests for DB bootstrap and auth logic.
5. Wire dashboard actions (`send_notification`, `manage_users`, etc.) to real views and logic.

## Contributors

| Name | GitHub |
|------|--------|
| Joseph Egan | [MachineCreations](https://github.com/MachineCreations) |
| Justin Crump | [ZipTy319](https://github.com/ZipTy319) |
| Nkobula Monzali | [PCC-NM](https://github.com/PCC-NM) |
| Lloyd Truong | [Profile](https://github.com/) |

## License

This project is distributed under the terms listed in `LICENSE`.