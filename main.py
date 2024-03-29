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

def window_menu(m_list):
    return choicebox('Menu:', 'Menu', m_list)

def window_show_pbook():
    curs.execute("SELECT * FROM phone_book")
    conn.commit()
    db_in_list = curs.fetchall()
    db_in_str = db_to_str(db_in_list)
    print(db_in_str)
    textbox('Contacts:\n\nName Surname\t\t\tPhone number\t\tEmail', 'Contacts', db_in_str)

def window_import():
    while 1:
        import_path = fileopenbox('Choose a file ', 'Import', filetypes=["*.db"])
        if import_path == None:
            break
        elif import_path[-3:] == ".db":
            if import_path[-len(db_path):] == db_path:
                msgbox('Эта база данных уже используется\n(Поробуйте переименовать файл)', 'WARNING')
            else:
                with open(db_path, 'w') as db, open(import_path, 'r') as import_file:
                    for line in import_file:
                        db.write(line)
                conn = sl.connect(db_path)
                curs = conn.cursor()
                db_init()
                msgbox("База данных была импортирована успешно!", "SUCCESS!")
                break
        elif import_path != None:
            msgbox("AHTUNG!\nВыберите файл с расширением .db", "WARNING")

def window_search():
    search = enterbox('Введите имя, фамилию, номер или почту контакта, полную информацию которого хотите найти:', 'SEARCH' )
    curs.execute(f"SELECT * FROM phone_book WHERE name = '{search}' OR surname = '{search}' OR main_ph_num = '{search}' OR email = '{search}'")
    list = curs.fetchall()
    print(list)
    if list != None:
        list_in_str = db_to_str(list)
        textbox('Contacts:\n\nName Surname\t\t\tPhone number\t\tEmail', 'Contacts', list_in_str)
    else:
        msgbox('Такой информации нет в вашей контактной книге', 'EROR')

def db_to_str(list):
    str = ""
    id = 0
    for line in list:
        id += 1
        if line[4] == None:
            email = "------"
        else:
            email = line[4]
        str += f"{id}. {line[1]} {line[2]}\t\t\t{line[3]}\t\t{email}\n"
    return str
################################################################################################
######################################## INITIALIZATION ########################################
################################################################################################
db_path = 'ph_book.db'
conn = sl.connect(db_path)
curs = conn.cursor()

menu_list = ['Exit', 'Show phone book', 'Import phone book', 'Search contact']

##############################################################################################
######################################## MAIN PROGRAM ########################################
##############################################################################################
db_init()

# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num, email) VALUES ('Petea', 'Pupkin', '012345678', 'sobaka@mail.ru');")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num) VALUES ('Vasea', 'Pupkin', '012345678');")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num) VALUES ('Igor', 'Vremea', '876543210');")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num, email) VALUES ('Svinka', 'Pepa', '012345678', 'pios@mail.ru');")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num, email) VALUES ('Rick', 'Sanches', '012345678', '0_0@mail.net');")
# curs.execute("INSERT INTO phone_book (name, surname, main_ph_num) VALUES ('Igor', 'Vremea', '876543210');")


while 1:
    choice = window_menu(menu_list)
    print(choice)
    match choice:
        case 'Exit' | None:
            break
        case 'Show phone book': 
            window_show_pbook()
        case 'Import phone book':
            window_import()
        case 'Search contact':
            window_search()

