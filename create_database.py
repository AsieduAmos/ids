import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

sql = """
DROP TABLE IF EXISTS Details;
CREATE TABLE Details(
           name text,id_no integer PRIMARY KEY, relationship text 
);
"""
c.executescript(sql)

conn.commit()











































conn.close()