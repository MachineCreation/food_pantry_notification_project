# Food Pantry Notification Project

Desktop app prototype for food pantry communication workflows.

## Contributors

| Name | GitHub |
|------|--------|
| Joseph Egan | [MachineCreations](https://github.com/MachineCreations) |
| Justin Crump | [ZipTy319](https://github.com/ZipTy319) |
| Nkobula Monzali | [PCC-NM](https://github.com/PCC-NM) |
| Lloyd Truong | [Profile](https://github.com/) |

## Overview

This repository is an early-stage Python desktop application using:

- Tkinter for GUI orchestration
- SQLite for local data storage
- `bcrypt` for password hashing
- `python-dotenv` for environment-based configuration

## Current Status

Project maturity: prototype / not in active development.

Implemented:

- Main app entry point and GUI bootstrapping
- `Database` helper class for SQLite connections and queries
- `User` model with authentication helper that checks credentials against database

In progress:

- Rebuild database function that creates and populates tables in the database
- Complete multi-screen routing and frame implementations
- End-to-end sign-in/sign-up workflows
- Notification features (send/log/template/user-management)
- Automated tests

## Requirements

- Python 3.14
- Tkinter support in your Python installation
- Windows PowerShell (commands below are written for PowerShell)

## Quick Start

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Environment Configuration

Create a `.env` file in the project root to override defaults:

```env
DATABASE_URL=app/database/database.db
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

If `.env` is not present, fallback defaults from `env.py` are used.

## Repository Layout

```text
food_pantry/
|-- main.py
|-- env.py
|-- requirements.txt
|-- app/
|   |-- database/
|   |   |-- models/
|   |   |   `-- Database.py
|   |   `-- setup/
|   |       `-- create_database.py
|   |-- gui/
|   |   |-- GUI.py
|   |   `-- utilities/
|   |       |-- routes.py
|   |       `-- models/
|   |           `-- FrameBase.py
|   `-- logic/
|       `-- models/
|           `-- User.py
|-- LICENSE
`-- README.md
```

## Entry Points

- App runtime: `main.py`
- Database bootstrap logic: `app/database/setup/create_database.py`

## Database Bootstrap Behavior

The rebuild flow:

- Creates `database.db` if it does not exist
- Drops and recreates `roles`
- Seeds `roles` with `admin`, `subscriber`, `member`
- Drops and recreates `users`
- Creates an admin user from environment values
- Seeds a few dummy users for development

## Notes For Developers

- GUI controller lives in `app/gui/GUI.py`.
- Route dispatch helper lives in `app/gui/utilities/routes.py`.
- DB access utility is `app/database/models/Database.py`.
- Authentication helper model is `app/logic/models/User.py`.
- Dependencies are listed in `requirements.txt`.

## Suggested Next Steps

1. Complete database creation bootstrap.
2. Finalize route table and frame classes for each view.
3. Implement persistent sign-up flow.
4. Wire sign-in UI to real credential checks via `User.authenticate`.
5. Add tests for database rebuild and auth paths.
6. Add CI checks (lint + tests).


## License

This project is distributed under the terms listed in `LICENSE`.