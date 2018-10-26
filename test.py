import sqlite3


connection = sqlite3.connect('data.db')

# cursor is going to run a query and store the result
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'jose', 'asdf')

users = [
  (1, 'jose', 'asdf'),
  (2, 'juan', 'fdsa'),
  (3, 'Caroline', 'blabla'),
]

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
select_query = "SELECT * FROM users"

# cursor.execute(insert_query, user)
cursor.executemany(insert_query, users)

# for row in cursor.execute(select_query):
#   print(row)


# When we insert changes, we must tell the connection to save them to the disk (the data.db file)
connection.commit() 

connection.close()

