import re
import sqlite3   
conn = sqlite3.connect("orders.db")   # connection from database
cursor = conn.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS orders (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user TEXT NOT NULL,
#         order_details TEXT NOT NULL,
#         status TEXT DEFAULT 'pending'
#     )
# """)
# conn.commit()

cursor.execute("SELECT * FROM orders")
orders = cursor.fetchall()

for order in orders:
    print(type(order))

# t1=('biryani :','spice :','150')
# st1=' '.join(t1)
# print(orders)
# t1=('1','mutton','150')
# st1=''
# for order in t1: 
#     st1 +=str(order) +' '

# print(st1)


conn.close()