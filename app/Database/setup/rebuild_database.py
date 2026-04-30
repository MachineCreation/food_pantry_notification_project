#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:rebuild_database.py
# Author: Justin Crump
# 2026-04-29
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Utility script to rebuild database tables if they do not exist

# Local Imports
from app.Database.models.t_database import Database

# Python Imports

def create_table() -> None:
    """
    Create all required database tables if they do not already exist.
    THis script is intended as a setup utility and is not part of normal runtime
    """
    with Database.connect() as conn:
        cursor = Database.cursor()

    """
    ROLES Table
    """
    cursor.execute("""
    IF NOT EXISTS (
        SELECT * 
        FROM    sysobjects 
        WHERE   name='ROLES' 
        AND xtype='U'
        )
        
        CREATE TABLE ROLES (
            role_id INTEGER IDENTITY(1,1)   PRIMARY KEY,
            role    NVARCHAR(30) NOT NULL
                CONSTRAINT  chk_valid_role  CHECK (role IN ('subscriber', 'member', 'admin'))
                CONSTRAINT  def_role        DEFAULT 'subscriber'
                );""")
    print("Roles table created successfully")

    """
    IMAGES Table
    """
    cursor.execute("""
    IF NOT EXISTS (
        SELECT * 
        FROM    sysobjects 
        WHERE   name='IMAGES' 
        AND xtype='U'
        )
        
        CREATE TABLE IMAGES (
            image_id        INTEGER IDENTITY(1,1)   PRIMARY KEY,
            image_location  NVARCHAR(MAX)   NOT NULL
            );""")
    print("Images table created successfully")

    """
    USERS Table
    """
    cursor.execute("""
    IF NOT EXISTS (
        SELECT * 
        FROM    sysobjects 
        WHERE   name='USERS' 
        AND xtype='U'
        )
        
        CREATE TABLE USERS (
            user_id         INTEGER IDENTITY(1,1)     PRIMARY KEY,
            first_name      NVARCHAR(100)   NOT NULL,
            last_name       NVARCHAR(100)   NOT NULL,
            username        NVARCHAR(255)   NOT NULL,
            email_address   NVARCHAR(255)   NOT NULL UNIQUE,
            password_hash   NVARCHAR(MAX)   NOT NULL,
            role_id         INTEGER         NOT NULL,
                CONSTRAINT  fk_role_id   FOREIGN KEY (role_id) 
                    REFERENCES ROLES(role_id)
            );""")
    print("Users table created successfully")

    """
    TEMPLATE Table
    """
    cursor.execute("""
    IF NOT EXISTS (
    SELECT *
    FROM    sysobjects 
    WHERE   name='TEMPLATE'
    AND     xtype='U'
    )
    CREATE TABLE TEMPLATE (
        template_id     INTEGER IDENTITY(1,1)         PRIMARY KEY,
        template_name   NVARCHAR(255)   NOT NULL UNIQUE,
        creator_id      INTEGER         NOT NULL,
        subject         NVARCHAR(255)   NOT NULL,
        tags            NVARCHAR(MAX)   NOT NULL,
            CONSTRAINT fk_creator_id    FOREIGN KEY (creator_id)
                REFERENCES USERS(user_id)
                );""")
    print("Template table created successfully")

    """
    NOTIFICATIONS Table
    """
    cursor.execute("""
    IF NOT EXISTS (
    SELECT *
    FROM    sysobjects
    WHERE   name='NOTIFICATIONS'
    AND     xtype='U'
    )
    
    CREATE TABLE NOTIFICATIONS (
        notification_id     INTEGER IDENTITY(1,1)    PRIMARY KEY,
        sender_id           INTEGER     NOT NULL,
        template_id         INTEGER     NOT NULL,
        subject             NVARCHAR(255)   NOT NULL,
        body_text           NVARCHAR(MAX)   NOT NULL,
        num_recip           INTEGER     NOT NULL,
        image_id            INTEGER     NOT NULL,
        date_time           DATETIME    NOT NULL,
            CONSTRAINT fk_sender_id     FOREIGN KEY (sender_id)
                REFERENCES USERS(user_id),
            CONSTRAINT fk_template_id   FOREIGN KEY (template_id)
                REFERENCES TEMPLATE(template_id),
            CONSTRAINT fk_image_id      FOREIGN KEY (image_id)
                REFERENCES IMAGES(image_id)
                );""")
    print("Notifications table created successfully")

    """
    Starter Data
    """

    cursor.execute("""
    INSERT INTO ROLES (role)
        VALUES ('subscriber'), ('member'), ('admin');
    """)
    print("Roles data added safely")

    cursor.execute("""
    INSERT INTO IMAGES (image_location)
        VALUES ('/images/welcome.png'), ('/images/alert.png'), ('/images/news.png');
    """)
    print("Images data added safely")

    cursor.execute("""
    INSERT INTO USERS (first_name, last_name, username, email_address, password_hash, role_id)
        VALUES ('Alice', 'Johnson', 'alicej', 'alice@example.com', 'hash1', 1),
            ('Bob', 'Smith', 'bobsmith', 'bob@example.com', 'hash2', 2),
            ('Carol', 'Davis', 'carold', 'carol@example.com', 'hash3', 3);
    """)
    print("Users data added safely")

    cursor.execute("""
    INSERT INTO TEMPLATE (template_name, creator_id, subject, tags)
        VALUES ('WelcomeTemplate', 3, 'Welcome to our service', 'welcome,intro'),
            ('AlertTemplate', 2, 'Important Alert', 'alert,system');
    """)
    print("Template data added safely")

    cursor.execute("""
    INSERT INTO NOTIFICATIONS (sender_id, template_id, subject, body_text, num_recip, image_id, date_time)
        VALUES (3, 1, 'Welcome!', 'Thanks for joining our platform.', 1, 1, '2024-01-15T10:30:00'),
            (2, 2, 'System Alert', 'Please review the latest system update.', 3, 2, '2025-07-21T05:30:00'),
            (1, 1, 'Greetings', 'We are glad to have you here.', 2, 3, '2026-03-11T12:30:00');
    """)
    print("Notification data added safely")

    Database.connect().commit()


if __name__ == "__main__":
    create_table()
    print("Database rebuild complete.")

