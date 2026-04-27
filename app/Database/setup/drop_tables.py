from app.Database.models.t_database import Database

def drop_table():
    cursor = Database.cursor()

    cursor.execute("DROP TABLE IF EXISTS NOTIFICATIONS")
    Database.connect().commit()
    print("NOTIFICATIONS dropped")

    cursor.execute("DROP TABLE IF EXISTS TEMPLATE")
    Database.connect().commit()
    print("TEMPLATE dropped")

    cursor.execute("DROP TABLE IF EXISTS USERS")
    Database.connect().commit()
    print("USERS dropped")

    cursor.execute("DROP TABLE IF EXISTS IMAGES")
    Database.connect().commit()
    print("IMAGES dropped")

    cursor.execute("DROP TABLE IF EXISTS ROLES")
    Database.connect().commit()
    print("ROLES dropped")

if __name__ == '__main__':
    drop_table()