# Food Pantry Notification Project

Desktop application project for managing food pantry notifications. The current codebase is an early-stage Python application built around a Tkinter GUI, a SQLite database layer, and room for notification, template, login, and review-log features under the `app/GUI` package.

## Current Status

This repository currently includes:

- A Tkinter application entry point in `main.py`
- A database wrapper in `app/Database/models/Database.py`
- A database creation script in `app/Database/setup/create_database.py`
- Placeholder GUI subpackages for login/logout, notification sending, template creation, and review logging

The main GUI shell exists, but most end-user functionality is still under development.

## Project Structure

```text
food_pantry_notification_project/
|-- main.py
|-- env.py
|-- requirements.txt
|-- test.py
|-- app/
|   |-- Database/
|   |   |-- models/
|   |   |   `-- Database.py
|   |   `-- setup/
|   |       `-- create_database.py
|   |-- GUI/
|   |   |-- GUI.py
|   |   |-- login_out/
|   |   |-- review_log/
|   |   |-- send_notification/
|   |   `-- template_creation/
|   `-- Logic/
`-- LICENSE
```

## Requirements

- Python 3.14 is referenced in the source file shebangs
- `tkinter` for the desktop GUI
- `sqlite3` from the Python standard library
- `bcrypt`
- `python-dotenv`

If you want to install the core third-party packages directly:

```powershell
pip install -r requirements.txt
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Optionally create a `.env` file for local configuration.
4. Initialize the database.
5. Launch the app.

Example on Windows PowerShell:

```powershell
python -m venv venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
python main.py
```

## Configuration

The project loads environment variables through `python-dotenv` and expects values for the database path and default admin credentials.

Example `.env` file:

```env
DATABASE_URL=app/Database/database.db (this value is set for now)
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

Notes:

- `.env` is ignored by git.
- The SQLite database file `app/Database/database.db` is also ignored by git.
- The helper functions to create the default admin user and dummy users exist in the database setup module, but they are not called automatically by the current `main()` setup flow.

## Database Initialization

Run the database bootstrap script through `test.py`:

```powershell
python rebuild_database.py
```

This currently:

- Creates `app/Database/database.db` if it does not already exist
- Creates the `roles` table
- Inserts the default roles: `admin`, `subscriber`, and `member`
- Creates the `users` table

## Running The Application

Start the Tkinter application with:

```powershell
python main.py
```

This opens the root window and instantiates the `GUI` class from `app/GUI/GUI.py`.

## Development Notes

- `app/GUI/GUI.py` currently defines the main GUI shell, but widget construction is still a placeholder.
- `app/Logic/` exists for non-UI application logic but is not populated yet.
- The codebase is organized for future separation between GUI, business logic, and database access.

## License

This project is distributed under the terms in `LICENSE`.