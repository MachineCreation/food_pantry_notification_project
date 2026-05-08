from app.database.setup.drop_tables import drop_table
from app.database.setup.create_database import create_table

if __name__ == "__main__":
    drop_table()
    create_table()
