#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: create_database
# Author: Joseph Egan
# 2026-04-17
# Sources: None
# Contributors:
# -------------------------------------------------------------------------------
# Description: simple script to create and populate tables in the Database
# directory

# Local imports
from app.database.models.Database import Database

# python imports
import bcrypt

def main():
    database: Database = Database()
    make_users(database)
    

def make_users(database):
    '''
    make some users for testing
    '''
    users = [
        [
            "McFly",
            "gggggggg",
            "McFly@yesterday.now",
            "Marty",
            "McFly",
            False,
            "Rock Creek"
        ],
        [
            "Doc",
            "gggggggg",
            "Doc@future.now",
            "Emmett",
            "Brown",
            False,
            "Cascade",
            2
        ],
        [
            "Einstein",
            "gggggggg",
            "Einstein@past.now",
            "Albert",
            "Einstein",
            False,
            "Sylvania"
        ],
        [
            "admin",
            "gggggggg",
            "admin@now.now",
            "Admin",
            "User",
            True,
            "Southeast",
            3
        ]
    ]

    for user in users:
        database.sign_up_user(*user)

def replace_passwords(database):
    '''
    helper function to replace all passwords in the database with a known
    password for testing
    '''
    database.execute_query(
        '''
        UPDATE USERS
        SET password = ?
        WHERE password_hash IN (hash1, hash2, hash3)
        ''',
        (bcrypt.hashpw("gggggggg".encode('utf-8'), bcrypt.gensalt(12)),)
    )