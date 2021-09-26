import sqlite3

db_connection = sqlite3.connect('database.db')

with open('static/sql_tables/transactions.sql') as f:
    print(f)
    db_connection.executescript(f.read())
    print(f.__str__)
    print('Executed: {}'.format(f.name))

with open('static/sql_tables/items.sql') as f:
    db_connection.executescript(f.read())
    print('Executed: {}'.format(f.name))

with open('static/sql_tables/product_categories.sql') as f:
    db_connection.executescript(f.read())
    print('Executed: {}'.format(f.name))

with open('static/sql_tables/sections.sql') as f:
    print('Executed: {}'.format(f.name))

with open('static/sql_tables/subproduct_categories.sql') as f:
    print('Executed: {}'.format(f.name))

with open('static/sql_tables/tr_details.sql') as f:
    print('Executed: {}'.format(f.name))



cur = db_connection.cursor()

cur.execute("INSERT INTO product_categories (pr_category, pr_desc) values (?, ?)",
               ('A', 'Groceries'))
cur.execute("INSERT INTO product_categories (pr_category, pr_desc) values (?, ?)",
               ('B', 'Health'))
cur.execute("INSERT INTO product_categories (pr_category, pr_desc) values (?, ?)",
               ('C', 'Shopping'))




cur.execute("INSERT INTO transactions (trans_type, trans_descr, trans_exec_date) values (?, ?, ?)",
               ('I', 'Income', '2021-05-21'))

cur.execute("INSERT INTO transactions (trans_type, trans_descr, trans_exec_date) values (?, ?, ?)",
               ('E', 'Expense', '2021-06-24'))

db_connection.commit()
db_connection.close()               

