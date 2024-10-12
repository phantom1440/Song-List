import sqlite3 

con = sqlite3.connect('Songs.sqlite')


cursor = con.cursor()

query = ''' CREATE TABLE songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    photo VARCHAR(255) NOT NULL
)'''


cursor.execute(query)