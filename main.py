from functions import *
import sqlite3 as sl

######## FUNCTIONS ########
#
# show_list(list)
#
###########################

conn = sl.connect('ph_book.db')
curs = conn.cursor()
curs.execute("""
            CREATE TABLE IF NOT EXISTS phone_book(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            main_ph_num TEXT,
            others_ph_nums TEXT,
            email TEXT
            )
            """)

# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num, email) VALUES ('Petea', 'Pupkin', '012345678', 'sobaka@mail.ru');")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num) VALUES ('Vasea', 'Pupkin', '012345678')")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num) VALUES ('Igor', 'Vremea', '876543210')")
# conn.commit()
curs.execute("SELECT * FROM phone_book")
list = curs.fetchall()
show_list(list)



