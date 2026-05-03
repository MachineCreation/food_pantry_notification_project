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

DATABASE_URL = os.getenv("DATABASE_URL") or 'app/Database/database.db'

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME") or 'admin'
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL") or 'admin@example.com'
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or 'admin123'
