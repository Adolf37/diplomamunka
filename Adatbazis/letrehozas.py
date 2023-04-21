import sqlite3

conn = sqlite3.connect('diplomamunka.db')

c = conn.cursor()
c.execute("""
    CREATE TABLE videok ( 

        id INTEGER PRIMARY KEY, 
        video BLOB NOT NULL,
        videoNeve TEXT NOT NULL
        
       );
""")
print('Adatbazis letrehozva')
c.close()