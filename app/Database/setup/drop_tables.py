#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:drop_tables.py
# Author: Justin Crump
# 2026-04-29
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Utility script to drop database tables if they do not exist

# Local Imports
from app.Database.models.t_database import Database

# Python Imports

def drop_table() -> None:
    """
    Drop all database tables used by the application.
    This script is intended for development / reset purposes only.
    """
    # Connection for all operations
    with Database.connect() as conn:
        cursor = conn.cursor()

    # Drop in dependency-safe order (child -> parent)
    cursor.execute("DROP TABLE IF EXISTS NOTIFICATIONS")
    print("NOTIFICATIONS dropped")

    cursor.execute("DROP TABLE IF EXISTS TEMPLATE")
    print("TEMPLATE dropped")

    cursor.execute("DROP TABLE IF EXISTS USERS")
    print("USERS dropped")

    cursor.execute("DROP TABLE IF EXISTS IMAGES")
    print("IMAGES dropped")

    cursor.execute("DROP TABLE IF EXISTS ROLES")
    print("ROLES dropped")

if __name__ == '__main__':
    drop_table()
    print("Database cleanup complete.")