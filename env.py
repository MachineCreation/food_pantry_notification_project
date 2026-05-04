#! usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:env.py
# Author: Lloyd Truong
# 2026-04-23
# Sources: None
# Contributors: 
# -------------------------------------------------------------------------------
# Description: basic environment injection for app configuration

# Local imports

# python imports
import dotenv, os

dotenv.load_dotenv()

DB_HOST = os.getenv("DB_HOST") or "cisdbss.pcc.edu"
DB_USER = os.getenv("DB_USER") or "CIS234A_Pi"
DB_NAME = os.getenv("DB_NAME") or "CIS234A_Pi"
DB_PASS = os.getenv("DB_PASS") or "Planet$"

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME") or 'admin'
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL") or 'admin@example.com'
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or 'admin123'
