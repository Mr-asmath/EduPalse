import sqlite3

def execute_query(database):
    try:
        # Connect to the SQLite database (or create one if it doesn't exist)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        
        # Read SQL query from user input
        query = input("Enter your SQL query: ")
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch and display results if it's a SELECT query
        if query.strip().lower().startswith("select"):
            column_names = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            
            # Print table headers
            print(" | ".join(column_names))
            print("-" * (len(" | ".join(column_names)) + 5))
            
            # Print table rows
            for row in results:
                print(" | ".join(str(value) for value in row))
        else:
            # Commit changes if it's an INSERT, UPDATE, or DELETE query
            conn.commit()
            print("Query executed successfully.")

    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    database_name = "db.sqlite3"  # Change this to your database file
    while True:
        execute_query(database_name)
