import sqlite3

db_connection = sqlite3.connect('database.db')

with open('static/sql_tables/items.sql') as f:
    print(f)
    db_connection.executescript(f.read())
    print(f.__str__)
    print('Executed: {}'.format(f.name))

"""
cur = db_connection.cursor()

cur.execute("INSERT INTO items (acc_name, acc_type) values (?, ?)",
               ('Eurobank', 'Debit'))
cur.execute("INSERT INTO items (acc_name, acc_type) values (?, ?)",
               ('Peiraios', 'Debit'))
cur.execute("INSERT INTO items (acc_name, acc_type) values (?, ?)",
               ('Ticket Rest', 'Debit'))

"""
db_connection.commit()
db_connection.close()               

