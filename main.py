import sqlite3

# Connect to the SQLite database file
connection = sqlite3.connect('./instance/Formula1.sqlite')

# Create a cursor object
cursor = connection.cursor()

# Execute SQL queries
# cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('John Doe', 25))

# Commit the changes
# connection.commit()

# Fetch data (optional)
# cursor.execute("SELECT * FROM users")

cursor.execute('SELECT * FROM constructors LIMIT 10')
rows = cursor.fetchall()

for row in rows:
    for x in row:
        print(str(x), end=" | ")
    print("")

# cursor.execute("DELETE FROM constructors WHERE constructorId IN('8', '9')")
# cursor.fetchall()

# cursor.execute('SELECT * FROM constructors LIMIT 10')
# rows = cursor.fetchall()

# print("After deletion")
for row in rows:
    for x in row:
        print(str(x), end=" | ")
    print("")


# Close the connection
connection.close()
