import sqlite3

db_conn = sqlite3.connect(library_database.db)

db_conn.execute("""INSERT INTO authors (name, email)
                values ('Gerry', 'gerry@gmail.com')                
                
""")
db_conn.commit()