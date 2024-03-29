import sqlite3 as sl
from easygui import *

###########################################################################################
######################################## FUNCTIONS ########################################
###########################################################################################
#                  (->) == (return) 
#
# db_init()                                     // database initialization
# db_to_str(list)       -> str                  // list with database info converts to a single str
# window_menu(list)     -> id(int) of choice    // window menu
# 

def db_init():
    curs.execute("""
                CREATE TABLE IF NOT EXISTS phone_book(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                main_ph_num TEXT,
                email TEXT
                )
                """)
    
def window_show_pbook():
    curs.execute("SELECT * FROM phone_book")
    conn.commit()
    db_in_list = curs.fetchall()
    db_in_str = db_to_str(db_in_list)
    print(db_in_str)
    textbox('Contacts:\n\nName Surname\t\t\tPhone number\t\tEmail', 'Contacts', db_in_str)

def window_menu(m_list):
    return choicebox('Menu:', 'Menu', m_list)


def db_to_str(list):
    str = ""
    for line in list:
        if line[4] == None:
            email = "------"
        else:
            email = line[4]
        str += f"{line[0]}. {line[1]} {line[2]}\t\t\t{line[3]}\t\t{email}\n"
    return str
################################################################################################
######################################## INITIALIZATION ########################################
################################################################################################
conn = sl.connect('ph_book.db')
curs = conn.cursor()

menu_list = ['Exit', 'Show phone book', ]


# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num, email) VALUES ('Petea', 'Pupkin', '012345678', 'sobaka@mail.ru');")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num) VALUES ('Vasea', 'Pupkin', '012345678');")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num) VALUES ('Igor', 'Vremea', '876543210');")


##############################################################################################
######################################## MAIN PROGRAM ########################################
##############################################################################################
db_init()
while 1:
    choice = window_menu(menu_list)
    print(choice)
    match choice:
        case 'Exit' | None:
            break
        case 'Show phone book': 
            window_show_pbook()

