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
    db_in_list = db_to_list()

def window_menu(m_list):
    return choicebox('Menu:', 'Menu', m_list)

def window_show_pbook(list):
    db_in_str = db_to_str(list)
    textbox('Contacts:\n\nName Surname\t\t\tPhone number\t\tEmail', 'Contacts', db_in_str)

def window_import():
    msgbox('ВНИМАНИЕ!\nКонтакты добавляются даже, если есть уже в вашей записной книге (дубликаты)', 'IMPORTANT')
    while 1:
        import_path = fileopenbox('Choose a file ', 'Import', filetypes=["*.db"])
        if import_path == None:
            break
        elif import_path[-3:] == ".db":
            try:
                conn_import = sl.connect(import_path)
                curs_import = conn_import.cursor()
                curs_import.execute('SELECT * FROM phone_book')
            except sl.OperationalError:
                msgbox('Нужная таблица контактов не найдена.\nВыберите другую базу данных.', 'EROR')
                continue
            conn_import.commit()
            import_list = curs_import.fetchall()
            for i in import_list:
                curs.execute(f"INSERT INTO phone_book (name, surname, main_ph_num, email) VALUES ('{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}')")
            msgbox("База данных была импортирована успешно!", "SUCCESS!")
            break
        elif import_path != None:
            msgbox("AHTUNG!\nВыберите файл с расширением .db", "WARNING")

def window_export():
    while 1:
        save_file_path = filesavebox('Выберите куда хотите экспортировать книгу:', 'SAVE')
        print(save_file_path)
        if save_file_path == None:
            break
        elif save_file_path[-3:] != '.db':
            msgbox('AHTUNG!\nВыберите файл с разрешением .db', 'WARNING')
            continue
        else:
            sf = open(save_file_path, 'w')
            sf.close()
            conn_exp = sl.connect(save_file_path)
            curs_exp = conn_exp.cursor()
            curs_exp.execute("""
                CREATE TABLE IF NOT EXISTS phone_book(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                main_ph_num TEXT,
                email TEXT
                )
                """)
            db_in_list = db_to_list()
            for i in db_in_list:
                curs_exp.execute(f"INSERT INTO phone_book (name, surname, main_ph_num, email) VALUES ('{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}')")
            conn_exp.commit()
            msgbox('✔️Экспорт успешно завершен', 'SUCCESS')
            break


def window_search():
    search = enterbox('Введите имя, фамилию, номер или почту контакта, полную информацию которого хотите найти:', 'SEARCH' )
    curs.execute(f"SELECT * FROM phone_book WHERE name = '{search}' OR surname = '{search}' OR main_ph_num = '{search}' OR email = '{search}' ORDER BY name,surname")
    list = curs.fetchall()
    if list != None:
        window_show_pbook(list)
    else:
        msgbox('Такой информации нет в вашей контактной книге', 'EROR')

def window_change():
    db_in_list = db_to_list()
    temp_list = [f"{i+1}. {db_in_list[i][1]} {db_in_list[i][2]}               {db_in_list[i][3]}               {db_in_list[i][4]}" for i in range(len(db_in_list))]
    choice = choicebox('Выберите контакт, данные которого хотите изменить:', 'CHANGE', temp_list )
    if choice != '' and choice != None:
        temp_id = int(choice.split('.')[0])-1
        changed_contact = multenterbox('Введите данные контакта:', 'CONTACT CHANGE', ['Имя','Фамилия', 'Номер телефона', 'почта'], [db_in_list[temp_id][1], db_in_list[temp_id][2], db_in_list[temp_id][3], db_in_list[temp_id][4]])
        curs.execute(f"UPDATE phone_book SET name = '{changed_contact[0]}', surname = '{changed_contact[1]}', main_ph_num = '{changed_contact[2]}', email = '{changed_contact[3]}' WHERE id = {db_in_list[temp_id][0]}")
        conn.commit()

def window_delete():
    db_in_list = db_to_list()
    temp_list = [f"{i+1}. {db_in_list[i][1]} {db_in_list[i][2]}               {db_in_list[i][3]}               {db_in_list[i][4]}" for i in range(len(db_in_list))]
    choice = choicebox('Выберите контакт, данные которого хотите изменить:', 'CHANGE', temp_list )
    if choice != '' and choice != None:
        temp_id = int(choice.split('.')[0])-1
        curs.execute(f"DELETE FROM phone_book WHERE id = {db_in_list[temp_id][0]}")
        conn.commit()

def window_add():
    new_contact = multenterbox('Введите данные контакта:', 'CONTACT CHANGE', ['Имя','Фамилия', 'Номер телефона', 'почта'])
    curs.execute(f"INSERT INTO phone_book (name, surname, main_ph_num, email) VALUES ('{new_contact[0]}', '{new_contact[1]}', '{new_contact[2]}', '{new_contact[3]}')")
    conn.commit()

def db_to_list():
    curs.execute("SELECT * FROM phone_book ORDER BY name,surname")
    conn.commit()
    return curs.fetchall()

def db_to_str(list):
    str = ""
    id = 0
    for line in list:
        id += 1
        if line[4] == None or line[4] == '':
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
db_in_list = []

menu_list = ['Show phone book', 'Add new contact', 'Search contact', 'Change contact', 'Delete contact', 'Import phone book', 'Export phone book', 'Exit']

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
    match choice:
        case 'Exit' | None:
            break
        case 'Show phone book': 
            db_in_list = db_to_list()
            window_show_pbook(db_in_list)
        case 'Add new contact':
            window_add()
        case 'Import phone book':
            window_import()
        case 'Export phone book':
            window_export()
        case 'Search contact':
            window_search()
        case 'Change contact':
            window_change()
        case 'Delete contact':
            window_delete()

