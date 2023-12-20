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
cursor.execute('select  d.forename, d.surname, r.year , r.name, ds.position, ds.points, bestLap.time '
            ' from drivers d'
            ' join driver_standings ds on d.driverId = ds.driverId'
            ' join races r on ds.raceId = r.raceId'
            ' join ('
            ' SELECT l.raceId, l.driverId, MIN(l.time) AS time FROM laptimes l GROUP BY l.raceId, l.driverId'
            ' ) AS bestLap'
            ' ON bestLap.raceId = r.raceId AND bestLap.driverId = d.driverId'
            ' where d.driverId = 15 '
            ' order by position '
            ' limit 10')
# nationality_filter = ''
# res = cursor.execute(
#     'SELECT COUNT(*) FROM drivers WHERE 1=1 AND (CASE WHEN "" = ?  THEN 1=1 ELSE nationality=? END)',
#     (nationality_filter, nationality_filter)).fetchone()[0]

# print(res)


rows = cursor.fetchall()
for row in rows:
    for x in row:
        print(str(x), end=" | ")
    print("")

# Close the connection


connection.close()
