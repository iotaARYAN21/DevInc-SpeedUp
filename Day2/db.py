import sqlite3

# Initialize SQLite connection
def create_connection():
    conn = sqlite3.connect("todos.db")
    return conn

# Create todos table if it doesn't exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    # cursor.execute("DROP TABLE IF EXISTS todos")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Pending', 'Completed')) ,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) 
        ) 
    """)  # the status line will only allow to enter Pending or Completed and for anything else it will throw an error
    conn.commit()
    conn.close()

def create_users_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   hashed_password TEXT NOT NULL
                   )
""")
    conn.commit()
    conn.close()

def add_user_id_column():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            ALTER TABLE todos ADD COLUMN user_id INTEGER NOT NULL
        """)
        conn.commit()
    except sqlite3.OperationalError:
        # If the column already exists, ignore the error
        pass
    finally:
        conn.close()


# Run this to create the table
if __name__ == "__main__":
    create_table()
    create_users_table()
    add_user_id_column()
