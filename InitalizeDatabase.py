import sqlite3

# Initalize and build the database


buildFile = open('BuildMainDB.sql')
buildScript = buildFile.read()

connection = sqlite3.connect(r"RedditArchive.db")
cursor = connection.cursor()

cursor.execute(buildScript)
connection.commit()

connection.close()





