#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:drop_tables.py
# Author: Justin Crump
# 2026-04-29
# Sources:
# Contributors: Joseph Egan
# -------------------------------------------------------------------------------
# Description: Utility script to drop database tables if they do not exist

# Local Imports
from app.database.models.Database import Database

# Python Imports


def drop_table() -> None:
    """
    Drop all database tables used by the application.
    This script is intended for development / reset purposes only.
    """
    # Connection for all operations
    database = Database()

    # Drop in dependency-safe order (child -> parent)
    database.execute_query("DROP TABLE IF EXISTS NOTIFICATIONS")
    print("NOTIFICATIONS dropped")

    database.execute_query("DROP TABLE IF EXISTS TEMPLATE")
    print("TEMPLATE dropped")

    database.execute_query("DROP TABLE IF EXISTS USERS")
    print("USERS dropped")

    database.execute_query("DROP TABLE IF EXISTS IMAGES")
    print("IMAGES dropped")

    database.execute_query("DROP TABLE IF EXISTS ROLES")
    print("ROLES dropped")
