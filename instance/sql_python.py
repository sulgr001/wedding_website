import sqlite3

# Connect to the database
conn = sqlite3.connect('rsvp.db')

# Create a cursor
cursor = conn.cursor()

# Query the data
cursor.execute("SELECT * FROM rsvp")

# Print all rows
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
