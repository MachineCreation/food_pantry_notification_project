# -------------------------------------------------------------------------------
# filename: create_database
# Author: Lloyd Truong
# 2026-04-23
# Sources: None
# Contributors: 
# -------------------------------------------------------------------------------
# Description: simple script to create a sqlite3 database in the Database 
# directory

# Local imports
from app.Database.models.Database import Database

# python imports
import sqlite3
from pathlib import Path
from bcrypt import hashpw, gensalt

def main():
    '''
    construct database in the Database directory
    '''
    # find the path to the Database directory
    directory = find_database_directory_path()
    
    if directory is None:
        print("Database directory not found.")
        return
    
    # make database file if it does not exist
    create_database_file(directory)
    
    # create a Database instance and connect to it
    database = Database()
    database.connect()
    database.make_cursor()

    # create tables
    create_roles_table(database)
    fill_roles_table(database)
    create_users_table(database)
    create_admin_user(database)
    fill_dummy_users(database)

    database.disconnect()

# --------------------------------- functions --------------------------------
def find_database_directory_path():
    '''
    search for the app/Database directory
    '''
    target_directory_name = "Database"
    current_directory = Path(__file__).parent

    # condition to stop if it hits root directory or target directory
    while current_directory.name != target_directory_name and \
    current_directory.parent != current_directory:
        
        current_directory = current_directory.parent

    
    if current_directory.name == target_directory_name:
        return current_directory
    else:
        return None

# --------------------    
def create_database_file(directory: Path):
    '''
    create the sqlite3 database file in the Database directory
    '''
    db_path = directory / "database.db"
    if not db_path.exists():
        connection = sqlite3.connect(db_path)
        connection.close()
        print(f"New database created at {db_path}")


# --------------------    
def create_roles_table(database: Database):
    '''
    create roles table for app role management
    '''
    if not database:
        print("No database instance provided.")
        return
    
    database.drop_table("roles")
    
    create_roles_table_query = """
    CREATE TABLE IF NOT EXISTS roles (
        role_name TEXT NOT NULL UNIQUE
    );
    """
    database.execute_query(create_roles_table_query)
    print("Table roles created successfully.")

# --------------------
def fill_roles_table(database: Database):
    '''
    fill roles table with default roles
    '''
    if not database:
        print("No database instance provided.")
        return
    
    default_roles = ["admin", "subscriber", "member"]
    for role in default_roles:
        insert_role_query = "INSERT OR IGNORE INTO roles (role_name) VALUES (?);"
        database.execute_query(insert_role_query, (role,))
    print("Table roles filled successfully.")

# --------------------
def create_users_table(database: Database):
    '''
    create user for app and role management
    '''
    if not database:
        print("No database instance provided.")
        return
    
    database.drop_table("users")
    
    create_user_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('admin', 'subscriber', 'member'))
    );
    """
    database.execute_query(create_user_table_query)
    print("Table users created successfully.")

# --------------------
def create_admin_user(database: Database):
    '''
    create default admin user for the app
    '''
    import env
    if not database:
        print("No database instance provided.")
        return
    
    username = env.ADMIN_USERNAME
    email = env.ADMIN_EMAIL
    password = env.ADMIN_PASSWORD
    hashed_password = hashpw(password.encode('utf-8'), gensalt(12)).decode('utf-8')
    role = "admin"

    insert_admin_query = """
    INSERT OR IGNORE INTO users (username, email, password, role)
    VALUES (?, ?, ?, ?);
    """
    database.execute_query(insert_admin_query, (username, email, hashed_password, role))
    print("Default admin user created successfully.")

# ----------------------
def fill_dummy_users(database: Database):
    '''
    fill users table with dummy users for testing
    '''
    if not database:
        print("No database instance provided.")
        return
    
    dummy_users = [
        ("user1", "user1@example.com", "password1", "subscriber"),
        ("user2", "user2@example.com", "password2", "member"),
        ("user3", "user3@example.com", "password3", "subscriber")
    ]

    for username, email, password, role in dummy_users:
        hashed_password = hashpw(password.encode('utf-8'), gensalt(12)).decode('utf-8')
        insert_user_query = """
        INSERT OR IGNORE INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?);
        """
        database.execute_query(insert_user_query, (username, email, hashed_password, role))
