# Food Pantry Notification Project

Desktop application for food pantry communication workflows. The app is built with Python and Tkinter, with a SQL Server backend.

## Contributors

| Name | GitHub |
|------|--------|
| Joseph Egan | [MachineCreations](https://github.com/MachineCreations) |
| Justin Crump | [ZipTy319](https://github.com/ZipTy319) |
| Nkobula Monzali | [PCC-NM](https://github.com/PCC-NM) |
| Lloyd Truong | [Profile](https://github.com/) |

## Overview

This repository contains a desktop GUI app that currently supports:

- sign-in / sign-up entry flow
- route-based frame navigation
- dashboard shell
- notification log screen
- send-notification screen
- template creation screen
- input validation utilities
- SQL Server database connection and basic user auth/signup operations
- database setup, rebuild, and seed helper scripts

## For Users

This app is intended for food pantry staff who need a desktop tool to manage sign-in, create and send notifications, review notification logs, and build reusable templates.

## For Developers

This repository is intended for developers who want to run, maintain, or extend the application. The main setup points are the Python environment, `.env` configuration, `main.py` for startup, and the database helper scripts in the project root.

## Tech Stack

- Python 3.14
- Tkinter (GUI)
- SQL Server via `pymssql`
- `python-dotenv` for environment variables
- `bcrypt` for password hashing

## Requirements

- Python 3.14
- Access to a SQL Server instance
- PowerShell (commands below use Windows PowerShell)

## Configuration

Environment values are loaded from `.env` through `env.py`.

Example `.env`:

```env
DATABASE_URL=your_sql_server_host
DB_NAME=your_database_name
DB_USERNAME=your_username
DB_PASSWORD=your_password
```

## Quick Start

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Database Scripts

The repository includes utility scripts for schema reset and seed operations:

- `rebuild_database.py` drops and recreates tables
- `populate_users.py` runs setup logic from `app/database/setup/create_database.py`

Run schema rebuild:

```powershell
python rebuild_database.py
```

Important:

- `app/database/setup/create_database.py` imports `USER_INFO` from `user_info.py`.
- If `user_info.py` is not present in your local copy, create it before running seed/rebuild utilities.

Example expected shape for `USER_INFO`:

```python
USER_INFO = {
	"admin": {
		"first_name": "Admin",
		"last_name": "User",
		"username": "admin",
		"email": "admin@example.com",
		"password": "ChangeMe123",
		"allergies": False,
		"campus": "Main",
		"role": 3,
	}
}
```

## Routes Currently Registered

From `app/gui/utilities/routes.py`:

- `sign_in`
- `sign_up`
- `sign_in_up_choice`
- `dashboard`
- `notification_log`
- `send_notification`
- `create_template`

## Testing

This project currently uses a script-based test harness.

- `test.py` runs `tests/test_run.py`
- validation tests are in `tests/test_validation.py`
- database behavior tests are in `tests/test_database.py`

Run tests:

```powershell
python test.py
```

Note: these tests are not a full `pytest` assertion suite yet. They are functional checks printed by the custom runner.

## Project Layout

```text
food_pantry_notification_project/
|-- LICENSE
|-- README.md
|-- env.py
|-- main.py
|-- rebuild_database.py
|-- requirements.txt
|-- test.py
|-- user_info.py
|-- app/
|   |-- database/
|   |   |-- models/
|   |   |   |-- Database.py
|   |   |   |-- LogRecordSQL.py
|   |   |   `-- Notifier.py
|   |   `-- setup/
|   |       |-- create_database.py
|   |       `-- drop_tables.py
|   |-- gui/
|   |   |-- GUI.py
|   |   |-- dashboard/
|   |   |   |-- models/
|   |   |   |   |-- DashBoard.py
|   |   |   |   `-- MessageSettings.py
|   |   |   `-- ui/
|   |   |       |-- dashboard.ui
|   |   |       `-- message_settings.ui
|   |   |-- log_in_out/
|   |   |   |-- models/
|   |   |   |   |-- SignIn.py
|   |   |   |   |-- SignInUpChoice.py
|   |   |   |   `-- SignUp.py
|   |   |   `-- ui/
|   |   |       |-- sign_in.ui
|   |   |       |-- sign_up.ui
|   |   |       `-- signin_up_choice.ui
|   |   |-- notification_log/
|   |   |   `-- NotificationLog.py
|   |   |-- send_notification/
|   |   |   |-- models/
|   |   |   |   `-- SendNotification.py
|   |   |   `-- ui/
|   |   |       |-- send_notification.ui
|   |   |       `-- send_notification_old.ui
|   |   |-- template_creation/
|   |   |   |-- models/
|   |   |   |   |-- template_controller.py
|   |   |   |   |-- template_frame.py
|   |   |   |   `-- template_view.py
|   |   |   `-- ui/
|   |   |       `-- template.ui
|   |   `-- utilities/
|   |       |-- EntryBehavior.py
|   |       |-- ToolTip.py
|   |       |-- routes.py
|   |       `-- models/
|   |           `-- FrameBase.py
|   `-- logic/
|       |-- models/
|       |   |-- LogRecord.py
|       |   |-- Notification.py
|       |   |-- Template.py
|       |   |-- Template_logic.py
|       |   `-- User.py
|       `-- utilities/
|           `-- validation.py
`-- tests/
    |-- test_database.py
    |-- test_log_record.py
    |-- test_log_record_sql.py
    |-- test_notification_log_logic.py
    |-- test_run.py
    |-- test_template.py
    `-- test_validation.py
```

## License

This project is distributed under the terms in `LICENSE`.