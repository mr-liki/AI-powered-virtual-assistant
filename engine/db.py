import sqlite3

conn = sqlite3.connect("lilly.db")
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key,name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES(null,'git','C:\\Program Files\\Git\\git-cmd')"
# cursor.execute(query)
# conn.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key,name VARCHAR(100),url VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO web_command VALUES(null,'linkedin','https://www.linkedin.com/')"
# cursor.execute(query)
# conn.commit()


# query = "DROP TABLE sys_command"
# cursor.execute(query)
