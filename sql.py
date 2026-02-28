import sqlite3

# Step 1: Establish a connection to the database
# This will create 'data.db' if it doesn't already exist.
connection = sqlite3.connect("data.db")

# Step 2: Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Step 3: Create the table schema
# We'll create a simple table named 'STUDENT'
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT(
    NAME VARCHAR(25), 
    CLASS VARCHAR(25), 
    SECTION VARCHAR(25), 
    MARKS INT
);
"""
cursor.execute(table_info)

# Step 4: Insert records into the table
# We add a few rows of data for the AI to query later
cursor.execute("INSERT INTO STUDENT VALUES('Aryan', 'Data Science', 'A', 90)")
cursor.execute("INSERT INTO STUDENT VALUES('Mehak', 'Data Science', 'B', 100)")
cursor.execute("INSERT INTO STUDENT VALUES('Vikram', 'DevOps', 'A', 86)")
cursor.execute("INSERT INTO STUDENT VALUES('Sanya', 'AI', 'C', 95)")

# Step 5: Save (Commit) your changes and close
print("Records inserted successfully!")
connection.commit()
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)
connection.close()