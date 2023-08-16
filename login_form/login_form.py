
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import hashlib
from turtle import home
from sql.db_connect import *
import mysql.connector as database
from fnct.getpath import Get_Local_Path
from PIL import Image, ImageTk
import os

current_directory = Get_Local_Path()
global rights_dict
rights_dict = {}
global version
version = '1.0.2'

def refresh(self):
    self.destroy()
    self.__init__()

def validate_login(uname, input_password):
    db_password = ""
    try:
        from sql.db_data_functions import SQL_Connect
        conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)
    except database.Error as e:
        print(f"Nie udało się połączyć z bazą danych MariaDB: {e}")

    try:
        get_db_password = conn.cursor()
        get_db_password.execute("SELECT haslo FROM konta WHERE login='%s'" % uname)
        db_password = get_db_password.fetchall()[0][0]
    except Exception as e:
        print("Error 77")
        print(e)
    if hashlib.sha256(input_password.encode()).hexdigest() == db_password:
        return True
    else:
        return False

def login():
    global uname
    uname=username.get()
    pwd=password.get()
    home_directory = os.path.expanduser('~')
    home_directory = os.path.join(home_directory, "Documents", "PajerApp")
    if os.path.exists(home_directory) == False:
        os.system('mkdir %s' % home_directory)
    pajer_file = os.path.join(home_directory, "lastlogin.txt")
    #applying empty validation
    if uname=='' or pwd=='':
        message.set("Wpisz proszę login i hasło")
    else:
        if validate_login(uname, pwd) == True:

            main_window.deiconify()
            login_screen.destroy()
#            from pajer import Create_Employee_Tab
#            Create_Employee_Tab()

            global rights_dict
            rights_dict = {}
            from sql.db_data_functions import SQL_Connect
            conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)
            get_rights = conn.cursor()
            get_rights.execute("SELECT uprawnienia, departments, rm_emp, add_emp, rm_ent, add_ent, cities, tl FROM konta WHERE login='%s'" % uname)
            user_rights = get_rights.fetchall()
            rights_dict['uprawnienia'] = user_rights[0][0]
            try:
                rights_dict['departments'] = user_rights[0][1].split(",")
            except:
                rights_dict['departments'] = user_rights[0][1]
            rights_dict['rm_emp'] = user_rights[0][2]
            rights_dict['add_emp'] = user_rights[0][3]
            rights_dict['rm_ent'] = user_rights[0][4]
            rights_dict['add_ent'] = user_rights[0][5]
            try:
                rights_dict['cities'] = user_rights[0][6].split(",")
            except:
                rights_dict['cities'] = user_rights[0][6]
            rights_dict['tl'] = user_rights[0][7]

            try:
                myfile = open(pajer_file,"w")
                myfile.write(uname)
                myfile.close()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                print(e)
                pass

            from Pajer import Create_Menu
            Create_Menu()


        else:
            message.set("Nieprawidłowe dane logowania.")

def login_form():
    home_directory = os.path.expanduser('~')
    home_directory = os.path.join(home_directory, "Documents", "PajerApp")
    pajer_file = os.path.join(home_directory, "lastlogin.txt")
    global login_screen
    try:
        tmpvariable07 = uname
    except:
        login_screen = Toplevel()
        login_screen.resizable(False, False)
        login_screen.iconbitmap(current_directory + "\img\\favicon.ico")
        login_screen.title("Logowanie")
        login_screen.geometry("320x332")
        imgpath = current_directory + "\img\logo2.png"
        logo = PhotoImage(file=imgpath)

        try:
            myfile = open(pajer_file,"r")
            savedlogin = myfile.read()
            myfile.close()
        except:
            pass

    #declaring variable
        global message;
        global username
        global password
        username = StringVar()
        password = StringVar()
        message = StringVar()
        
        try:
            username.set(savedlogin)
        except:
            pass

        canvas1 = Canvas(login_screen, width = 400, height = 400)
        canvas1.pack(fill = "both", expand = True)
        canvas1.create_image( 0, 0, image = logo, anchor = "nw")
        canvas1.image = logo
        #img_label = ttk.Label(login_screen, image=logo)
        #img_label.pack(side='top',  padx=5,  pady=5)
        #img_label.image = logo

        ttk.Label(canvas1, text="",textvariable=message, font=("Helvetica", 13, "bold"), foreground="red").pack(side='top',  padx=5,  pady=(5, 40))
        #ttk.Label(canvas1, text="Nazwa uzytkownika * ").pack(side='top',  padx=5,  pady=(40, 5))
        canvas1.create_text(160, 60, text="Nazwa użytkownika:", fill="black", font=('Helvetica 11 bold'))
        login1_entry = ttk.Entry(canvas1, textvariable=username)
        if 'savedlogin' not in locals():
            login1_entry.focus()
        login1_entry.pack(side='top',  padx=5,  pady=20)
        if 'savedlogin' not in locals():
            login1_entry.focus()
        #ttk.Label(canvas1, text="Haslo * ").pack(side='top',  padx=5,  pady=5)
        canvas1.create_text(160, 135, text="Hasło:", fill="black", font=('Helvetica 11 bold'))
        login_entry = ttk.Entry(canvas1, textvariable=password ,show="*")
        login_entry.bind("<Return>", (lambda event: login()))
        if 'savedlogin' in locals():
            login_entry.focus()
        login_entry.pack(side='top',  padx=5,  pady=(30,5))
        if 'savedlogin' in locals():
            login_entry.focus()
        ttk.Button(canvas1, text="Login",command=login).pack(side='top',  padx=5,  pady=15)



main_window = Tk()
main_window.iconbitmap(current_directory + "\img\\favicon.ico")
main_window.title("PaJer v%s - najlepszy program Rejestracji Czasu Pracy we wszechświecie" % version)
main_window.state('zoomed')