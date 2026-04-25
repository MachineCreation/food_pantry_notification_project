# Food Pantry Notification Project

This project is intended to be a desktop application for managing food pantry communication, account access, and role-based workflows.

## Contributors

| Name | GitHub |
|------|--------|
| Joseph Egan | [MachineCreations](https://github.com/MachineCreations) |
| Justin Crump | [ZipTy319](https://github.com/ZipTy319) |
| Nkobula Monzali | [PCC-NM](https://github.com/PCC-NM) |
| Lloyd Truong | [Profile](https://github.com/) |

## Project Vision

The goal of this repository is to provide a simple desktop system that helps a food pantry organization manage user access and send notifications to the right people at the right time.

The application is intended to support three main needs:

- secure user sign-in and sign-up
- role-based access for administrators, members, and subscribers
- a notification workflow for pantry-related communication

## Planned Features

The intended product scope includes:

- user account creation and authentication
- email or username based login
- password validation and secure password storage
- a dashboard that changes based on the user's role
- notification creation and sending tools
- notification history or logs
- template management for repeat messages
- administrative user management tools
- local database storage for application data

## Intended Users

This project is meant to support:

- administrators who manage users and system settings
- members who create or send pantry notifications
- subscribers who receive updates and access limited features

## Planned Tech Stack

The project is expected to use:

- Python as the primary programming language
- Tkinter for the desktop user interface
- SQLite for local data storage
- `python-dotenv` for configuration management
- `bcrypt` for password hashing

## Proposed Application Flow

The intended user flow is:

1. Launch the desktop application.
2. Choose to sign in or create an account.
3. Authenticate with a username or email and password.
4. Open a dashboard tailored to the user's role.
5. Access tools such as sending notifications, viewing logs, managing templates, or administering users.

## Planned Configuration

The project is expected to read environment values from a `.env` file for settings such as:

- database path
- default administrator credentials
- local development configuration

An example configuration may include:

```env
DATABASE_URL=app/Database/database.db
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

## Proposed Project Structure

This repository is intended to grow into a structure similar to the following:

```text
food_pantry/
|-- main.py
|-- env.py
|-- requirements.txt
|-- app/
|   |-- database/
|   |   |-- models/
|   |   `-- setup/
|   |-- gui/
|   |   |-- dashboard/
|   |   |-- logInOut/
|   |   |-- send_notifications/
|   |   |-- create_template/
|   |   |-- review_notification_log/
|   |   |-- manage_users/
|   |   `-- utilities/
|   `-- logic/
|       |-- models/
|       `-- utilities/
|-- LICENSE
`-- README.md
```

## Development Goals

1. Build a working desktop GUI for authentication and navigation.
2. Design a database schema for users, roles, and notifications.
3. Implement secure authentication and account creation.
4. Add dashboard screens for each role.
5. Build notification, template, and user-management workflows.
6. Add tests for validation, authentication, and database behavior.

## Long-Term Direction

The intended outcome is a maintainable desktop application that can serve as a course project and demonstrate:

- GUI design with Python
- layered application structure
- form validation and authentication
- database integration
- role-based feature access

## License

This project is distributed under the terms listed in `LICENSE`.