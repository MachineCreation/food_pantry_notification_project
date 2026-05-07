# Food Pantry Notification Project

Desktop application for a food pantry notification system built with Python and Tkinter. Enables volunteers and administrators to manage user accounts, send targeted notifications, and manage inventory for food pantry operations.

## Contributors

| Name | GitHub |
|------|--------|
| Joseph Egan | [MachineCreations](https://github.com/MachineCreations) |
| Justin Crump | [ZipTy319](https://github.com/ZipTy319) |
| Nkobula Monzali | [PCC-NM](https://github.com/PCC-NM) |
| Lloyd Truong | [Profile](https://github.com/) |

## Overview

This repository contains a desktop GUI application that is intended to support food pantry communication and account workflows. The current codebase focuses on:

- launching a Tkinter application shell
- routing between login, sign-up, and dashboard screens
- validating user input for authentication flows
- connecting application logic to a local SQLite-backed database layer

The project is still in progress. Some screens and routes exist only as placeholders, and parts of the authentication flow still fall back to temporary development behavior when the database layer is incomplete.

## Tech Stack

- Python 3.14
- Tkinter for the desktop UI
- SQLite for local persistence
- `python-dotenv` for environment configuration
- `bcrypt` for password hashing support

## Current State

**Fully Implemented:**

- `main.py` starts the desktop app and initializes the GUI
- `app/gui/GUI.py` creates the root window and app context
- `app/gui/utilities/routes.py` routes between the currently wired screens
- sign-in, sign-up, and sign-in/sign-up choice screens are present
- `app/gui/dashboard/models/DashBoard.py` provides the current dashboard frame
- `app/logic/models/User.py` contains authentication and sign-up helpers
- User input validation for authentication flows

**In Progress or Incomplete:**

- Complete database bootstrap and persistence layer
- Full account creation and login integration with database
- Dashboard destinations for notification, template, and user-management flows
- Comprehensive CI/CD pipeline setup

## Available Screens

The current route table includes these screen names:

- `sign_in`
- `sign_up`
- `sign_in_up_choice`
- `dashboard`

The dashboard UI also references future routes for notification and user-management features, but those routes are not yet registered in the route table.

## Testing

Basic test suite includes:

- `tests/test_database.py` - database operations and schema validation
- `tests/test_validation.py` - user input validation logic
- `tests/test_run.py` - application startup and basic flow tests

To run tests:

```powershell
python -m pytest tests/
```

Note: Test coverage is limited. Additional tests needed for authentication flows, database persistence, and GUI interactions.

## Requirements

- Python 3.14
- Tkinter support in the Python installation
- Windows PowerShell (for the quick start commands below)

## Quick Start

PowerShell:

```powershell
winget install Microsoft.msodbcsql.18
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Testing

Basic test suite includes:

- `tests/test_database.py` - database operations and schema validation
- `tests/test_validation.py` - user input validation logic
- `tests/test_run.py` - application startup and basic flow tests

To run tests:

```powershell
python -m pytest tests/
```

Note: Test coverage is limited. Additional tests needed for authentication flows, database persistence, and GUI interactions.

## Configuration

Environment values are loaded from `.env` through `env.py`. If a variable is not present, the project uses the fallback defaults defined there.

Example `.env`:

```env
DATABASE_URL=<database url>
DB_NAME=<database name>
DB_USERNAME=<database username>
DB_PASSWORD=<database password>
```

## Project Layout

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
|   |   |-- dashboard/
|   |   |   |-- models/
|   |   |   |   `-- DashBoard.py
|   |   |   `-- ui/
|   |   |       `-- dashboard.ui
|   |   |-- logInOut/
|   |   |   |-- models/
|   |   |   |   |-- SignIn.py
|   |   |   |   |-- SignInUpChoice.py
|   |   |   |   `-- SignUp.py
|   |   |   `-- ui/
|   |   |       |-- sign_in.ui
|   |   |       |-- sign_up.ui
|   |   |       |-- signin_up_choice.ui
|   |   |       `-- send_notification.ui
|   |   `-- utilities/
|   |       |-- EntryBehavior.py
|   |       |-- ToolTip.py
|   |       |-- routes.py
|   |       `-- models/
|   |           `-- FrameBase.py
|   `-- logic/
|       |-- models/
|       |   `-- User.py
|       `-- utilities/
|           `-- validation.py
|-- LICENSE
`-- README.md
```

## Notes For Developers

- `main.py` is the application entry point.
- `app/gui/GUI.py` owns the root window and application context.
- `app/gui/utilities/routes.py` is the route dispatcher.
- `app/logic/models/User.py` currently mixes real database calls with temporary fallback authentication values for development. For admin access
- `app/database/setup/create_database.py` exists as the intended database setup entry point, but it is not implemented yet.

## Development Priorities

1. Implement the database bootstrap script.
2. Register and build the remaining dashboard destination routes.
3. Add tests around validation, authentication, and database integration.

## License

This project is distributed under the terms listed in `LICENSE`.