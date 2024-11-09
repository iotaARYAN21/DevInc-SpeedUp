import sqlite3

# Initialize SQLite connection
def create_connection():
    conn = sqlite3.connect("todos.db")
    return conn

# Create todos table if it doesn't exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Pending', 'Completed'))  
        ) 
    """)  # the status line will only allow to enter Pending or Completed and for anything else it will throw an error
    conn.commit()
    conn.close()

# Run this to create the table
if __name__ == "__main__":
    create_table()
