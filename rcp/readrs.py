import serial
import os
import sys
from datetime import datetime
from time import strftime
import tkinter as tk
from tkinter.ttk import *
from tkinter import font as fnt
from time import sleep
import mysql.connector as database
from wakeonlan import send_magic_packet
import paramiko

#OPEN SERIAL PORT
ser = serial.Serial(
        port='COM7',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.2,
)
#CONNECT TO LOCAL DATABASE

def new_db_connect():
    global conn
    global cursor
    try:
        conn = database.connect(
            user="rcp",
            password="PDArcpSERWIS",
            host="10.0.10.1",
            database="RFID"
        )
        cursor = conn.cursor()
    except database.Error as e:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
        sys.exit(1)

try:
    conn = database.connect(
        user="rcp",
        password="PDArcpSERWIS",
        host="10.0.10.1",
        database="RFID"
    )
except database.Error as e:
    print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
    sys.exit(1)

cursor = conn.cursor()

def WakeComputer(card_id, conn):
    sql_query = "SELECT sprzet.mac, przypisanieip.ip FROM pracownicy LEFT JOIN przypisanieip ON przypisanieip.pracownik = pracownicy.id LEFT JOIN sprzet ON przypisanieip.komputer = sprzet.id WHERE pracownicy.karta = '" + card_id + "'"
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    mac_addr = get_sql.fetchall()[0][0]
    print(card_id)
    try:
        cmd_to_execute = "sudo etherwake -i enp3s0f0 " + mac_addr
    except Exception as e:
        print(e)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.10.1", username="wakeonlan", password="81d7a5c58", port=4224)
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
    except Exception as e:
        print(e)
    if card_id == "0004293363" or card_id == "0004102845":
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 88:51:FB:67:91:55")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 20:47:47:B5:00:C3")
    if card_id == "0004365562" or card_id == "0002002502" or card_id == "0004388356" or card_id == "0004427606" or card_id == "0004336582" or card_id == "0004176737" or card_id == "0002001285" or card_id == "0004328792" or card_id == "0004405307":
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 44:37:E6:6A:49:96")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 44:37:E6:AE:69:4D")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 44:37:E6:A3:8C:D9")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("sudo etherwake -i enp3s0f0 B8:27:EB:A2:31:4F")
    
#BASIC FUNCTIONS DEFINITIONS

#Wykryj w jakim systemie pracujesz i dopasuj ścieżki plików
def Get_Local_Path():
    localpath = os.getcwd()
    global logpath
    global imgpath
    if sys.platform.startswith("linux"):
        logpath = localpath + "/log/"
        imgpath = localpath + "/img/"
    elif sys.platform == "darwin":
        print("Jestem maczkiem")
    elif sys.platform == "win32":
        logpath = localpath + "\log\\"
        imgpath = localpath + "\img\\"
    else:
        print("Error 112 - nie można zdefiniować wersji systemu")
    print(logpath)
    print(imgpath)

Get_Local_Path()

#Dodatkowa funckja weryfikująca istnienie okna (przeczytany RS)
def Destroy_Window_Existance(Window):
    Window.destroy()
    global existance
    existance = None
    try:
        thinking_window.withdraw()
    except:
        pass

#Ustaw okno na fullscreen
def Window_Fullscreen(Window):
    Window.overrideredirect(True)
    Window.overrideredirect(False)
    Window.attributes('-fullscreen',True)

#Wyciągnij z bazy danych imię, nazwisko i ID przypisane do przeczytanej karty
def Get_SQL_Data(card_id):
    new_db_connect()
    try:
        file_object = open(logpath + 'karty.txt', 'w')
        file_object.write(card_id) #Wrzuć ostatnio zczytaną kartę
        file_object.close()
        global employee_id
        global employee_fname
        global employee_lname
        global success_check
        cursor.execute("SELECT id FROM pracownicy WHERE karta='%s'" % card_id)
        employee_id = cursor.fetchall()[0][0]
        cursor.execute("SELECT imie FROM pracownicy WHERE karta='%s'" % card_id)
        employee_fname = cursor.fetchall()[0][0]
        cursor.execute("SELECT nazwisko FROM pracownicy WHERE karta='%s'" % card_id)
        employee_lname = cursor.fetchall()[0][0]
        success_check = 1
    except:
        success_check = 0
        pass

#Wrzuć wpis do lokalnej bazy
def Insert_SQL_Local(employee_id, action_type):
    cursor.execute("INSERT INTO obecnosc (pracownik, action) VALUES (%s, %s)", (employee_id, action_type))
    conn.commit()
        
def Insert_SQL_Raspberry(employee_id, action_type):
    try:
        conn3 = database.connect(
        user="rcp",
        password="PDArcpSERWIS",
        host="10.0.10.16",
        database="RFID"
        )
        cursor3 = conn3.cursor()
        cursor3.execute("INSERT INTO obecnosc (pracownik, action) VALUES (%s, %s)", (employee_id, action_type))
        conn3.commit()
    except database.Error as e: #Nieudana próba podłączenia do bazy
        file_object = open(logpath + 'connectlog.txt', 'a')
        file_object.write(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}\n") #Wrzuć do logu powód braku połączenia
        file_object.close()
        file_object = open(logpath + 'accesslog.txt', 'a')
        file_object.write("INSERT INTO obecnosc (pracownik, time, action) VALUES(" + str(employee_id) + ", " + time_of_entry + ", " + str(action_type) + ");\n") #Wrzuć gotową SQLkę do pliku
        file_object.close()
    conn3.close()
        
#Wrzuć i zweryfikuj wpis w zdalnej bazie
def Insert_SQL_Remote(employee_id, action_type):
    global success_errow_window_type #Zmienna definiująca treść komunikatu po wrzuceniu wpisu
    time_of_entry = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    try: #Połączenie ze zdalną bazą i upload wpisu
        conn2 = database.connect(
        user="rcp",
        password="PDArcpSERWIS",
        host="10.0.10.1",
        database="RFID"
        )
        cursor2 = conn2.cursor()
        cursor2.execute("INSERT INTO obecnosc (pracownik, action) VALUES (%s, %s)", (employee_id, action_type))
        conn2.commit()
        #if action_type == 1:
        #    WakeComputer(card_id, conn2)
        actual_time = datetime.today().strftime('%Y-%m-%d')
        actual_hour = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        try: #Weryfikacja poprawności wpisu
            sql_check = "SELECT id FROM obecnosc WHERE action = " + str(action_type) + " AND pracownik = " + str(employee_id) + " AND time LIKE '" + actual_time + "%'"
            cursor2.execute(sql_check)
            result2 = cursor2.fetchall()
            if not result2: #Jeśli nie można zweryfikować - wrzuć do pliku gotowy SQL
                file_object = open(logpath + 'accesslog.txt', 'a')
                file_object.write("INSERT INTO obecnosc (pracownik, time, action) VALUES(" + str(employee_id) + ", " + str(actual_time) + ", " + str(action_type) + ");")
                file_object.close()
                success_errow_window_type = 21 #NIE MOZNA ZWERYFIKOWAC WPISU W ZDALNEJ BAZIE
            del result2 #Skasuj zmienną żeby w następnym cyklu nie wykryło jej błędnie
        except: #Brak połączenia z bazą - do logu (nie powinien ten błąd nigdy wystąpić)
            file_object = open(logpath + 'errorlog.txt', 'a')
            file_object.write(actual_hour + " Krytyczny blad\n")
            file_object.close()
        conn2.close()
    except database.Error as e: #Nieudana próba podłączenia do bazy
        file_object = open(logpath + 'connectlog.txt', 'a')
        file_object.write(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}\n") #Wrzuć do logu powód braku połączenia
        file_object.close()
        file_object = open(logpath + 'accesslog.txt', 'a')
        file_object.write("INSERT INTO obecnosc (pracownik, time, action) VALUES(" + str(employee_id) + ", " + time_of_entry + ", " + str(action_type) + ");\n") #Wrzuć gotową SQLkę do pliku
        file_object.close()
        success_errow_window_type = 11 #BRAK POLACZENIA ZE ZDALNA BAZA

#Połącz oba zapytania SQL żeby łatwiej było je wywołać
def Insert_SQL_All(employee_id, action_type):
#    Insert_SQL_Local(employee_id, action_type)
    Insert_SQL_Remote(employee_id, action_type)
#    Insert_SQL_Raspberry(employee_id, action_type)

#OKNO KOMUNIKAT PO WRZUCENIU WPISU DO BAZY
def Success_Error_Window(success_errow_window_type):
    Success_Error_Window = tk.Toplevel()
    Success_Error_Window.title("Rezultat")
    color = 'red'
    if success_errow_window_type == 42:
        string = "ERROR 42:\nJuż odnotowano\ndzisiejsze logowanie\n"
    elif success_errow_window_type == 43:
        string = "ERROR 43:\nŻeby wyjść z pracy,\nnajpierw do niej wejdź ;)"
    elif success_errow_window_type == 44:
        string = "ERROR 44:\nŻeby iść na przerwę,\nnajpierw wejdź do pracy ;)"
    elif success_errow_window_type == 45:
        string = "ERROR 45:\nŻeby wyjść z przerwy,\nnajpierw wejdź do pracy ;)"
    elif success_errow_window_type == 46:
        string = "ERROR 46:\nJuż dzisiaj\nwychodziłeś z pracy"
    elif success_errow_window_type == 47:
        string = "ERROR 47:\nJuż odnotowano\nwyjście na przerwę"
    elif success_errow_window_type == 48:
        string = "ERROR 48:\nJuż odnotowano\npowrót z przerwy"
    elif success_errow_window_type == 99:
        string = "ERROR 99:\nNie znaleziono\nkarty"
    elif success_errow_window_type == 67:
        string = "ERROR 67:\nNie można zweryfikować wpisu\nSpróbuj ponownie"
        color = 'orange'
    elif success_errow_window_type == 21:
        string = "ERROR 21:\nNIE MOZNA ZWERYFIKOWAC WPISU\nW ZDALNEJ BAZIE"
        color = 'orange'
    elif success_errow_window_type == 11:
        string = "ERROR 11:\nBRAK POLACZENIA ZE ZDALNA BAZA"
        color = 'orange'
    elif success_errow_window_type == 100:
        string = employee_fname + " " + employee_lname + "\nSUKCES:\nPomyslnie\nzarejestrowano wpis"
        color = 'green'
    Success_Error_Window_Label = tk.Label(Success_Error_Window, text=string, fg=color, font=(None, 42, 'bold'))
    Success_Error_Window_Label.place(relx=0.32, rely=0.40)
    Success_Error_Window.after(3000, lambda: Destroy_Window_Existance(Success_Error_Window))
    Window_Fullscreen(Success_Error_Window)
    if Success_Error_Window.winfo_exists() == True:
        global existance
        existance = True

# WERYFIKACJA WPISU, USTAWIENIE ZMIENNEJ ABY W OKNIE KOMUNIKATU BYŁA ODPOWIEDNIA TREŚĆ
def check_entry(employee_id, action_type):
    new_db_connect()
    thinking_window.deiconify()
    var = 0
    global success_errow_window_type
    cursor.execute("SELECT pracownik, action, time FROM obecnosc")
    query = cursor.fetchall()
    check_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT pracownik, action, time FROM obecnosc WHERE pracownik = " + str(employee_id) + " AND action = 1 AND time LIKE \'" + str(check_date) + "%\'")
    query2 = cursor.fetchall()
    for (pracownik, action, time) in query:
        test_var = 0
        if not query2 and (action_type == 2 or action_type == 3 or action_type == 4):
            test_var = 5
            var = 2
            success_errow_window_type = 41 #Pracownik jeszcze nie wszedł do pracy
        time = str(time)
        time = time[0:10]
        if pracownik == employee_id and action_type <= 2 and action_type == action and time == check_date:
	        var += 1 #WPIS ISTNIEJE
    if var == 0:
        Insert_SQL_All(employee_id, action_type)
        actual_time = datetime.today().strftime('%Y-%m-%d')
        new_db_connect()
        cursor.execute("SELECT id FROM obecnosc WHERE action='%s' AND pracownik='%s' AND time > '%s'" % (action_type, employee_id, actual_time))
        result = cursor.fetchall()
        if not result:
            success_errow_window_type = 67 #LOKALNIE SUKCES / ZDALNIE PORAŻKA
        else:
            success_errow_window_type = 100 #SUKCES
            del result
    else:
        if action_type == 1:
            success_errow_window_type = 42 #ZDUBLOWANY WPIS
        elif action_type == 2 and test_var == 5:
            success_errow_window_type = 43 #WYJSCIE - BRAK WEJSCIA
        elif action_type == 3 and test_var == 5:
            success_errow_window_type = 44 #PRZERWA WEJSCIE - BRAK WEJSCIA
        elif action_type == 4 and test_var == 5:
            success_errow_window_type = 45 #PRZERWA WYJSCIE - BRAK WEJSCIA
        elif action_type == 2:
            success_errow_window_type = 46 #ZDUBLOWANE WYJSCIE
        elif action_type == 3:
            success_errow_window_type = 47 #ZDUBLOWANE WYJSCIE NA PRZERWE
        elif action_type == 4:
            success_errow_window_type = 48 #ZDUBLOWANE WYJSCIE Z PRZERWY
    Success_Error_Window(success_errow_window_type)

#MAIN WINDOW
root = tk.Tk()
root.title('Main')
Window_Fullscreen(root)

#WAITING WINDOW
thinking_window = tk.Toplevel(root)
thinking_window.title("I am thinking")
thinking_window.withdraw()
thinking_img = tk.PhotoImage(file=imgpath + 'thinking.png')
thinking_lbl = Label(thinking_window, image=thinking_img)
thinking_lbl.pack(anchor = 'center')
Window_Fullscreen(thinking_window)

#DEFINE VARIABLES AGAINST REFERENCE ERRORS
Buttons_Window = None
existance = None

def Button_Window():
    #DEFINE WINDOW
    Window = tk.Toplevel(root)
    Window.title("Buttons")
    Window.after(3000, lambda: [Destroy_Window_Existance(Window), thinking_window.withdraw()])
    #DEFINE WINDOW LABELS AND WIDGETS
    enter_btn = tk.Button(Window, text="Wejscie", width=24, height=6, font = fnt.Font(size = 42), bg="#26580F", activebackground="#86DC3D", command= lambda: check_entry(employee_id, 1)).grid(row=1, column=0)
    exit_btn = tk.Button(Window, text="Wyjscie", width=24, height=6, font = fnt.Font(size = 42), bg="#D1001F", activebackground="#EE6B6E", command= lambda: check_entry(employee_id, 2)).grid(row=1, column=1)
    pause_start_btn = tk.Button(Window, text="Przerwa", width=24, height=6, font = fnt.Font(size = 42), bg="#C5C6D0", activebackground="#D9DDDC", command= lambda: check_entry(employee_id, 3)).grid(row=2, column=0)
    pause_end_btn = tk.Button(Window, text="Koniec przerwy", width=24, height=6, font = fnt.Font(size = 42), bg="#808B96", activebackground="#D9DDDC", command= lambda: check_entry(employee_id, 4)).grid(row=2, column=1)
    welcome = Label(Window, text="Witaj " + employee_fname + " " + employee_lname).grid(row=0, column=0)
    welcome2 = Label(Window, text="Numer karty: " + str(card_id)).grid(row=0, column=1)
    Window_Fullscreen(Window)
    #USTAWIENIE ZMIENNEJ UMOŻLIWIAJĄCEJ ZABLOKOWANIE CZYTANIA RS
    if Window.winfo_exists() == True:
        global existance
        existance = True

#GŁÓWNE OKNO PROGRAMU Z ZEGARKIEM
def Main_Window():
    global employee_id
    try:
        del employee_fname
        del employee_lname
        del employee_id
    except:
        pass
    string = "\nPrzyłóż kartę\n" + strftime('   %H:%M:%S')
    lbl.config(text = string)
    if (existance != True) and (ser.inWaiting() > 3):
        global card_id
        card_id=str(ser.readline())[2:12]
        Get_SQL_Data(card_id)
        if success_check == 1:
            #check_hour = int(datetime.now().strftime("%H"))
#            if check_hour in (6, 7, 8, 9, 10):
#                check_entry(employee_id, 1)
#            elif check_hour in (15, 16, 17, 18, 19, 20, 21, 22, 23):
#                check_entry(employee_id, 2)
#            else:
            Buttons_Window = Button_Window()
        else:
            success_errow_window_type = 99
            Success_Error_Window(success_errow_window_type)
            print(card_id)
    lbl.after(200, Main_Window)


img = tk.PhotoImage(file=imgpath + 'pp.png')
lbl = Label(root, image=img, compound='top', font = ('calibri', 45, 'bold'))
lbl.place(relx=0.35, rely=0.35)

Main_Window()

root.mainloop()
try:
    conn.close()
    conn2.close()
except:
    pass

