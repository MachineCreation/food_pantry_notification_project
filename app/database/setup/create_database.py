#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:rebuild_database.py
# Author: Justin Crump
# 2026-04-29
# Sources:
# Contributors: Joseph Egan
# -------------------------------------------------------------------------------
# Description: Utility script to rebuild database tables if they do not exist

# Local Imports
from app.database.models.Database import Database
from user_info import USER_INFO

# Python Imports
import bcrypt


def create_table() -> None:
    """
    Create all required database tables if they do not already exist.
    THis script is intended as a setup utility and is not part of normal runtime
    """
    database = Database()

    """
    ROLES Table
    """

    roles_table_query = """
    IF NOT EXISTS (
        SELECT *
        FROM    sysobjects
        WHERE   name='ROLES'
        AND xtype='U'
        )

        CREATE TABLE ROLES (
            role_id INTEGER IDENTITY(1,1)   PRIMARY KEY,
            role    NVARCHAR(30) NOT NULL
                CONSTRAINT  chk_valid_role  CHECK (role IN ('subscriber', 'member', 'admin', 'deleted'))
                CONSTRAINT  def_role        DEFAULT 'subscriber'
                );"""

    database.execute_query(
        roles_table_query
    )

    print("Roles table created successfully")

    """
    IMAGES Table
    """
    images_table_query = """
    IF NOT EXISTS (
        SELECT *
        FROM    sysobjects
        WHERE   name='IMAGES'
        AND xtype='U'
        )

        CREATE TABLE IMAGES (
            image_id        INTEGER IDENTITY(1,1)   PRIMARY KEY,
            image_location  NVARCHAR(MAX)   NOT NULL
            );"""
    database.execute_query(
        images_table_query
    )

    print("Images table created successfully")

    """
    USERS Table
    """
    users_table_query = """
        IF NOT EXISTS (
            SELECT 1
            FROM sys.objects
            WHERE object_id = OBJECT_ID(N'dbo.USERS')
            AND type = 'U'
        )
        BEGIN
            CREATE TABLE dbo.USERS (
                user_id         INT IDENTITY(1,1) PRIMARY KEY,
                first_name      NVARCHAR(100) NOT NULL,
                last_name       NVARCHAR(100) NOT NULL,
                username        NVARCHAR(255) NULL,
                email_address   NVARCHAR(255) NOT NULL UNIQUE,
                password_hash   NVARCHAR(MAX) NULL,
                allergies       BIT NOT NULL,
                campus          NVARCHAR(50) NULL,
                role_id         INT NOT NULL,

                CONSTRAINT fk_users_role_id
                    FOREIGN KEY (role_id)
                    REFERENCES dbo.ROLES(role_id)
            );
        END;
    """

    database.execute_query(
        users_table_query
    )

    print("Users table created successfully")

    """
    TEMPLATE Table
    """
    template_table_query = """
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
        template_body   NVARCHAR(300)   NOT NULL,
        tags            NVARCHAR(MAX)   NULL,
            CONSTRAINT fk_creator_id    FOREIGN KEY (creator_id)
                REFERENCES USERS(user_id)
                );"""

    database.execute_query(
        template_table_query
    )

    print("Template table created successfully")

    """
    NOTIFICATIONS Table
    """
    notifications_table_query = """
    IF NOT EXISTS (
    SELECT *
    FROM    sysobjects
    WHERE   name='NOTIFICATIONS'
    AND     xtype='U'
    )
    
    CREATE TABLE NOTIFICATIONS (
        notification_id     INTEGER IDENTITY(1,1)    PRIMARY KEY,
        sender_id           INTEGER     NOT NULL,
        template_id         INTEGER     NULL,
        subject             NVARCHAR(255)   NOT NULL,
        body_text           NVARCHAR(MAX)   NOT NULL,
        num_recip           INTEGER     NOT NULL,
        image_id            INTEGER     NULL,
        date_time           DATETIME    NOT NULL,
            CONSTRAINT fk_sender_id     FOREIGN KEY (sender_id)
                REFERENCES USERS(user_id),
            CONSTRAINT fk_template_id   FOREIGN KEY (template_id)
                REFERENCES TEMPLATE(template_id),
            CONSTRAINT fk_image_id      FOREIGN KEY (image_id)
                REFERENCES IMAGES(image_id)
                );"""

    database.execute_query(
        notifications_table_query
    )

    print("Notifications table created successfully")

    """
    Starter Data
    """

    roles_data_query = """
    INSERT INTO ROLES (role)
        VALUES ('subscriber'), ('member'), ('admin'), ('deleted');
    """

    database.execute_query(
        roles_data_query
    )

    print("Roles data added safely")

    images_data_query = """
    INSERT INTO IMAGES (image_location)
        VALUES ('/images/welcome.png'), ('/images/alert.png'), ('/images/news.png');
    """
    database.execute_query(
        images_data_query
    )

    print("Images data added safely")

    users_data_query = """
    INSERT INTO USERS (
        first_name,
        last_name,
        username,
        email_address,
        password_hash,
        allergies,
        campus,
        role_id
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    for user in USER_INFO.values():
        hashed_password = str(bcrypt
                              .hashpw(user["password"].encode('utf-8'),
                                      bcrypt.gensalt(12)).decode('utf-8'))
        database.execute_query(
            users_data_query,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                hashed_password,
                user["allergies"],
                user["campus"],
                user["role"]
            )
        )

    print("Users data added safely")

    template_data_query = """
    INSERT INTO TEMPLATE (template_name, creator_id, subject, template_body)
        VALUES ('WelcomeTemplate', 3, 'Welcome to our service', 'Welcome to the Pantry project. We look forward to seeing you.'),
            ('AlertTemplate', 2, 'Important Alert','This is an important test of the notification system.');
    """

    database.execute_query(
        template_data_query
    )

    print("Template data added safely")

    notifications_data_query = """
    INSERT INTO NOTIFICATIONS (sender_id, template_id, subject, body_text, num_recip, image_id, date_time)
        VALUES (3, 1, 'Welcome!', 'Thanks for joining our platform.', 1, 1, '2024-01-15T10:30:00'),
            (2, 2, 'System Alert', 'Please review the latest system update.', 3, 2, '2025-07-21T05:30:00'),
            (1, 1, 'Greetings', 'We are glad to have you here.', 2, 3, '2026-03-11T12:30:00');
    """

    database.execute_query(
        notifications_data_query
    )

    print("Notification data added safely")
