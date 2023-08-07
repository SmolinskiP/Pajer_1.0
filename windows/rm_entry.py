from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter.messagebox import askyesno
from sql.db_data_functions import Delete_SQL, Add_Break_SQL, Get_Hash, Change_Password_SQL, Add_EntryExit_SQL, Add_Holiday_SQL, Create_Dict, Add_Random_Entry_SQL, Get_Single_Emp, Edit_Emp_Data, Get_Right, Delete_Emp_SQL, Add_Comment_SQL, Add_Emp_SQL, Get_Name, Send_Overtime
from tkinter import *
import tkinter.ttk as ttk
from fnct.getpath import Get_Local_Path
from datetime import date, datetime
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes
from tktimepicker import constants
import hashlib, re, threading, wget, os, requests
import webbrowser
from pathlib import Path

current_directory = Get_Local_Path()
today = date.today()
yearmonthday = today.strftime("%Y-%m-%d")

def Changelog():
    webbrowser.open('https://p.pdaserwis.pl/pliki/update/changelog.txt')

def Change_Connection_Params():

    filepath = Get_Local_Path() + "\\sql\\params.txt"
    db_file = open(filepath, 'r')
    db_params = db_file.readlines()
    connection_dict = {}

    connection_dict['login'] = re.findall(r'"([^"]*)"', db_params[0])[0]
    connection_dict['password'] = re.findall(r'"([^"]*)"', db_params[1])[0]
    connection_dict['host'] = re.findall(r'"([^"]*)"', db_params[2])[0]
    connection_dict['db'] = re.findall(r'"([^"]*)"', db_params[3])[0]
    connection_dict['port'] = re.findall(r'"([^"]*)"', db_params[4])[0]
    db_file.close()

    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Baza")
    wnd.lift()
    wnd.attributes("-topmost", True)

    db_login = StringVar()
    db_password = StringVar()
    db_host = StringVar()
    db_db = StringVar()
    db_port = StringVar()

    db_login.set(connection_dict['login'])
    db_password.set(connection_dict['password'])
    db_host.set(connection_dict['host'])
    db_db.set(connection_dict['db'])
    db_port.set(connection_dict['port'])

    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 14, 'bold'), focusthickness=3, focuscolor='none')

    lbl_login = ttk.Label(wnd, text="Login", font=("Arial", 13, 'bold'))
    ent_login = ttk.Entry(wnd)
    lbl_password = ttk.Label(wnd, text="Hasło", font=("Arial", 13, 'bold'))
    ent_password = ttk.Entry(wnd, show="*")
    lbl_host = ttk.Label(wnd, text="Host", font=("Arial", 13, 'bold'))
    ent_host = ttk.Entry(wnd)
    lbl_db = ttk.Label(wnd, text="Baza", font=("Arial", 13, 'bold'))
    ent_db = ttk.Entry(wnd)
    lbl_port = ttk.Label(wnd, text="Port", font=("Arial", 13, 'bold'))
    ent_port = ttk.Entry(wnd)
    send_button = ttk.Button(wnd, text="Aktualizuj", style='my.TButton', command=lambda: Params_Act(ent_login.get(), ent_password.get(), ent_host.get(), ent_db.get(), ent_port.get()))

    lbl_login.pack(pady=5)
    ent_login.pack(pady=5)
    lbl_password.pack(pady=5)
    ent_password.pack(pady=5)
    lbl_host.pack(pady=5)
    ent_host.pack(pady=5)
    lbl_db.pack(pady=5)
    ent_db.pack(pady=5)
    lbl_port.pack(pady=5)
    ent_port.pack(pady=5)
    send_button.pack(pady=30, ipady=10, ipadx=10, padx=30)

    ent_login.insert(END, db_login.get())
    ent_password.insert(END, db_password.get())
    ent_host.insert(END, db_host.get())
    ent_db.insert(END, db_db.get())
    ent_port.insert(END, db_port.get())

    def Params_Act(login, password, host, db, port):
        try:
            filepath = Get_Local_Path() + "\\sql\\params.txt"
            db_file = open(filepath, 'w')
            db_file.write('dbLogin="%s"\n' % login)
            db_file.write('dbPassword="%s"\n' % password)
            db_file.write('dbHost="%s"\n' % host)
            db_file.write('dbDatabase="%s"\n' % db)
            db_file.write('dbPort="%s"' % port)
            db_file.close()
            messagebox.showinfo("Sukces", "Pomyślnie ustawiono nowe parametry połączenia")
            wnd.destroy()
        except Exception as e:
            messagebox.showerror("Błąd!", "Coś poszło nie tak:\n%s" % e)

def Remove_Entry(entry_id, frame, uname):
    if Get_Right(uname, "rm_ent") == False:
        messagebox.showwarning("Ostrzeżenie", "Brak uprawnień do usuwania wpisów\nSkontaktuj się z administratorem")
        return
    answer = askyesno(title='Usuwanie wpisu', message='Na pewno chcesz usunac wpis?\nID: %s' % entry_id)
    if answer == True:
        Delete_SQL("obecnosc", "id", entry_id)
        frame.destroy()
    else:
        print("Nie usuwam wpisu")

def Add_Break(selected_emp, employee_id, uname):
    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Przerwa")
    wnd.lift()
    wnd.attributes("-topmost", True)
    #wnd.geometry("320x332")

    topframe = Frame(wnd)
    midframe = Frame(wnd)
    leftframe = Frame(midframe)
    rightframe = Frame(midframe)
    dwnframe = Frame(wnd)

    topframe.pack(side=TOP, expand=True, fill="both")
    midframe.pack(side=TOP, expand=True, fill="both")
    leftframe.pack(side=LEFT, expand=True, fill="both")
    rightframe.pack(side=RIGHT, expand=True, fill="both")
    dwnframe.pack(side=TOP, expand=True, fill="both")

    lbl_date = ttk.Label(topframe, text="Wybierz datę:", font=("Arial", 13, 'bold'))
    cal = Calendar(topframe, font="Arial 17", selectmode='day', year=int(yearmonthday[0:4]),month=int(yearmonthday[5:7]),date=int(yearmonthday[8:10]))
    cal.selection_set(date(int(yearmonthday[0:4]),int(yearmonthday[5:7]),int(yearmonthday[8:10])))

    lbl_time = ttk.Label(topframe, text="Wybierz czas przerwy:", font=("Arial", 13, 'bold'))
    lbl_time_fr = ttk.Label(leftframe, text="OD:", font=("Arial", 13, 'bold'))
    lbl_time_to = ttk.Label(rightframe, text="DO:", font=("Arial", 13, 'bold'))

    time_picker_fr = AnalogPicker(leftframe, type=constants.HOURS24)
    time_picker_fr.setHours(8)
    time_picker_fr.setMinutes(1)

    time_picker_to = AnalogPicker(rightframe, type=constants.HOURS24)
    theme_to = AnalogThemes(time_picker_to)
    theme_to.setDracula()
    time_picker_to.setHours(15)
    time_picker_to.setMinutes(59)

    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 14, 'bold'), focusthickness=3, focuscolor='none')

    comment=StringVar()
    lbl_comment = ttk.Label(dwnframe, text="Dodaj komentarz (opcjonalnie)", font=("Arial", 11))
    add_comment = ttk.Entry(dwnframe, textvariable=comment)

    send_button = ttk.Button(dwnframe, text="Wyślij pracownika na przerwę", style='my.TButton', command=lambda wnd=wnd, emp_id=employee_id, unam=uname: Add_Break_SQL(emp_id, cal.get_date(), time_picker_fr.time(), time_picker_to.time(), unam, comment.get(), wnd))

    lbl_date.pack(pady=5)
    cal.pack(pady=5)
    ttk.Separator(topframe, orient='horizontal').pack(fill='x', pady=5)
    lbl_time.pack(pady=5)
    lbl_time_fr.pack(pady=5)
    lbl_time_to.pack(pady=5)
    time_picker_fr.pack(expand=True, fill="both")
    time_picker_to.pack(expand=True, fill="both")
    ttk.Separator(dwnframe, orient='horizontal').pack(fill='x', pady=5)
    lbl_comment.pack(pady=10)
    add_comment.pack(pady=10)
    send_button.pack(pady=30, ipady=10, ipadx=10)
    ttk.Label(wnd, text="Wybrany pracownik", font=("Arial", 13, 'bold')).pack(side=TOP)
    the_choosen_one = ttk.Entry(wnd, state= "disabled", font=("Arial", 13, 'bold'), justify='center', textvariable=selected_emp)
    the_choosen_one.pack(side=TOP, fill=BOTH, expan=False)

def Change_Password(uname):
    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 14, 'bold'), focusthickness=3, focuscolor='none')

    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Hasło")
    wnd.lift()
    wnd.attributes("-topmost", True)

    act_pass = Get_Hash(uname)

    old_pwd = StringVar()
    new_pwd = StringVar()
    new_pwd_confirm = StringVar()

    ttk.Label(wnd, text="Podaj stare hasło:", font=("Arial", 13, 'bold')).pack(side=TOP ,padx=10, pady=5)
    old_pwd_ent = ttk.Entry(wnd, show="*", font=("Arial", 13, 'bold'), justify='center', textvariable=old_pwd)
    old_pwd_ent.pack(side=TOP, padx=10, pady=5)

    ttk.Label(wnd, text="Podaj nowe hasło:", font=("Arial", 13, 'bold')).pack(side=TOP, padx=10, pady=5)
    new_pwd_ent = ttk.Entry(wnd, show="*", font=("Arial", 13, 'bold'), justify='center', textvariable=new_pwd)
    new_pwd_ent.pack(side=TOP, padx=10, pady=5)

    ttk.Label(wnd, text="Potwierdź nowe hasło:", font=("Arial", 13, 'bold')).pack(side=TOP, padx=10, pady=5)
    new_pwd_confirm_ent = ttk.Entry(wnd, show="*", font=("Arial", 13, 'bold'), justify='center', textvariable=new_pwd_confirm)
    new_pwd_confirm_ent.pack(side=TOP, padx=10, pady=5)
    
    def check(act, old, new, confirm, uname):
        if old == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" or new == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" or confirm == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":
            messagebox.showwarning("Puste pola", "Uzupełnij wszystkie pola!")
        elif new != confirm:
            messagebox.showwarning("Ostrzezenie", "Podane hasła różnią się od siebie!")
        elif act != old:
            messagebox.showwarning("Złe hasło", "Niepoprawne stare hasło!")
        elif old == new:
            messagebox.showwarning("To samo", "Nowe hasło jest identyczne jak stare!")
        else:
            Change_Password_SQL(uname, new)
            wnd.destroy()
            messagebox.showinfo(title="Sukces", message="Zmieniono hasło użytkownikowi '%s'" % uname)

    send_button = ttk.Button(wnd, text="Aktualizuj hasło", style='my.TButton', command=lambda uname=uname, act=act_pass: check(act, hashlib.sha256(old_pwd.get().encode()).hexdigest(), hashlib.sha256(new_pwd.get().encode()).hexdigest(), hashlib.sha256(new_pwd_confirm.get().encode()).hexdigest(), uname))
    send_button.pack(side=TOP, padx=30, pady=20, ipadx=5, ipady=5)

def Add_EntryExit(selected_emp, employee_id, uname, date_from, date_to):
    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Wejście/Wyjście")
    wnd.lift()
    wnd.attributes("-topmost", True)
    #wnd.geometry("320x332")

    topframe = Frame(wnd)
    toptopframe = Frame(topframe)
    topleftframe = Frame(toptopframe)
    toprightframe = Frame(toptopframe)
    midframe = Frame(wnd)
    leftframe = Frame(midframe)
    rightframe = Frame(midframe)
    dwnframe = Frame(wnd)

    topframe.pack(side=TOP, expand=True, fill="both")
    lbl_date = ttk.Label(topframe, text="Wybierz datę:", font=("Arial", 13, 'bold'))
    lbl_date.pack(pady=5)
    toptopframe.pack(side=TOP, expand=True, fill="both")
    toprightframe.pack(side=RIGHT, expand=True, fill="both")
    topleftframe.pack(side=LEFT, expand=True, fill="both")
    midframe.pack(side=TOP, expand=True, fill="both")
    leftframe.pack(side=LEFT, expand=True, fill="both")
    rightframe.pack(side=RIGHT, expand=True, fill="both")
    dwnframe.pack(side=TOP, expand=True, fill="both")

    
    cal_from = Calendar(topleftframe, font="Arial 13", selectmode='day', year=int(date_from[0:4]),month=int(date_from[5:7]),date=int(date_from[8:10]))
    cal_from.selection_set(date(int(date_from[0:4]),int(date_from[5:7]),int(date_from[8:10])))
    cal_to = Calendar(toprightframe, font="Arial 13", selectmode='day', year=int(date_to[0:4]),month=int(date_to[5:7]),date=int(date_to[8:10]))
    cal_to.selection_set(date(int(date_to[0:4]),int(date_to[5:7]),int(date_to[8:10])))

    lbl_dt_fr = ttk.Label(topleftframe, text="OD:", font=("Arial", 13, 'bold'))
    lbl_dt_to = ttk.Label(toprightframe, text="DO:", font=("Arial", 13, 'bold'))
    lbl_dt_fr.pack(side=TOP, pady=5)
    lbl_dt_to.pack(side=TOP, pady=5)

    lbl_time = ttk.Label(topframe, text="Wybierz czas:", font=("Arial", 13, 'bold'))
    lbl_time_fr = ttk.Label(leftframe, text="Wejście:", font=("Arial", 13, 'bold'))
    lbl_time_to = ttk.Label(rightframe, text="Wyjście:", font=("Arial", 13, 'bold'))

    time_picker_fr = AnalogPicker(leftframe, type=constants.HOURS24)
    time_picker_fr.setHours(8)
    time_picker_fr.setMinutes(0)

    time_picker_to = AnalogPicker(rightframe, type=constants.HOURS24)
    theme_to = AnalogThemes(time_picker_to)
    theme_to.setDracula()
    time_picker_to.setHours(16)
    time_picker_to.setMinutes(0)

    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 14, 'bold'), focusthickness=3, focuscolor='none')

    comment=StringVar()
    lbl_comment = ttk.Label(dwnframe, text="Dodaj komentarz (opcjonalnie)", font=("Arial", 11))
    add_comment = ttk.Entry(dwnframe, textvariable=comment)

    send_button = ttk.Button(dwnframe, text="Dodaj obecność", style='my.TButton', command=lambda wnd=wnd, emp_id=employee_id, unam=uname: Add_EntryExit_SQL(emp_id, cal_from.get_date(), cal_to.get_date(), time_picker_fr.time(), time_picker_to.time(), unam, comment.get(), wnd))

    
    cal_from.pack(pady=5, padx=5)
    cal_to.pack(pady=5, padx=5)
    ttk.Separator(topframe, orient='horizontal').pack(fill='x', pady=5)
    lbl_time.pack(pady=5)
    lbl_time_fr.pack(pady=5)
    lbl_time_to.pack(pady=5)
    time_picker_fr.pack(expand=True, fill="both")
    time_picker_to.pack(expand=True, fill="both")
    ttk.Separator(dwnframe, orient='horizontal').pack(fill='x', pady=5)
    lbl_comment.pack(pady=10)
    add_comment.pack(pady=10)
    send_button.pack(pady=30, ipady=10, ipadx=10)
    ttk.Label(wnd, text="Wybrany pracownik", font=("Arial", 13, 'bold')).pack(side=TOP)
    the_choosen_one = ttk.Entry(wnd, state= "disabled", font=("Arial", 13, 'bold'), justify='center', textvariable=selected_emp)
    the_choosen_one.pack(side=TOP, fill=BOTH, expan=False)

def Add_Holiday(selected_emp, employee_id, uname, date_from, date_to):
    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Urlop")
    wnd.lift()
    wnd.attributes("-topmost", True)
    #wnd.geometry("320x332")

    topframe = Frame(wnd)
    toptopframe = Frame(topframe)
    topleftframe = Frame(toptopframe)
    toprightframe = Frame(toptopframe)
    midframe = Frame(wnd)
    leftframe = Frame(midframe)
    rightframe = Frame(midframe)
    dwnframe = Frame(wnd)

    topframe.pack(side=TOP, expand=True, fill="both")
    lbl_date = ttk.Label(topframe, text="Wybierz datę:", font=("Arial", 13, 'bold'))
    lbl_date.pack(pady=5)
    toptopframe.pack(side=TOP, expand=True, fill="both")
    toprightframe.pack(side=RIGHT, expand=True, fill="both")
    topleftframe.pack(side=LEFT, expand=True, fill="both")
    midframe.pack(side=TOP, expand=True, fill="both")
    leftframe.pack(side=LEFT, expand=True, fill="both")
    rightframe.pack(side=RIGHT, expand=True, fill="both")
    dwnframe.pack(side=TOP, expand=True, fill="both")

    
    cal_from = Calendar(topleftframe, font="Arial 13", selectmode='day', year=int(date_from[0:4]),month=int(date_from[5:7]),date=int(date_from[8:10]))
    cal_from.selection_set(date(int(date_from[0:4]),int(date_from[5:7]),int(date_from[8:10])))
    cal_to = Calendar(toprightframe, font="Arial 13", selectmode='day', year=int(date_to[0:4]),month=int(date_to[5:7]),date=int(date_to[8:10]))
    cal_to.selection_set(date(int(date_to[0:4]),int(date_to[5:7]),int(date_to[8:10])))

    lbl_dt_fr = ttk.Label(topleftframe, text="OD:", font=("Arial", 13, 'bold'))
    lbl_dt_to = ttk.Label(toprightframe, text="DO:", font=("Arial", 13, 'bold'))
    lbl_dt_fr.pack(side=TOP, pady=5)
    lbl_dt_to.pack(side=TOP, pady=5)

    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 14, 'bold'), focusthickness=3, focuscolor='none')
    s.configure("my.TMenubutton", font=('Arial', 14, 'bold'))

    lbl_type = ttk.Label(midframe, text="Wybierz rodzaj urlopu:", font=("Arial", 13, 'bold'))

    holiday_dict = Create_Dict('_action', 'action')
    holiday_list = []
    reversed_dictionary = dict(map(reversed, holiday_dict.items()))
    for key in holiday_dict:
        if key <= 4:
            pass
        else:
            holiday_list.append(holiday_dict[key])

    holiday_type = StringVar()
    choose_type = ttk.OptionMenu(midframe, holiday_type, holiday_list[0], *holiday_list, style='my.TMenubutton')

    comment=StringVar()
    lbl_comment = ttk.Label(dwnframe, text="Dodaj komentarz (opcjonalnie)", font=("Arial", 11))
    add_comment = ttk.Entry(dwnframe, textvariable=comment)

    send_button = ttk.Button(dwnframe, text="Dodaj urlop", style='my.TButton', command=lambda wnd=wnd, emp_id=employee_id, unam=uname: Add_Holiday_SQL(emp_id, int(reversed_dictionary[holiday_type.get()]), cal_from.get_date(), cal_to.get_date(), unam, comment.get(), wnd))

    
    cal_from.pack(pady=5, padx=5)
    cal_to.pack(pady=5, padx=5)
    ttk.Separator(topframe, orient='horizontal').pack(fill='x', pady=5)
    lbl_type.pack(pady=10)
    choose_type.pack(pady=10)
    ttk.Separator(dwnframe, orient='horizontal').pack(fill='x', pady=15)
    lbl_comment.pack(pady=10)
    add_comment.pack(pady=10)
    send_button.pack(pady=30, ipady=10, ipadx=10)
    ttk.Label(wnd, text="Wybrany pracownik", font=("Arial", 13, 'bold')).pack(side=TOP)
    the_choosen_one = ttk.Entry(wnd, state= "disabled", font=("Arial", 13, 'bold'), justify='center', textvariable=selected_emp)
    the_choosen_one.pack(side=TOP, fill=BOTH, expan=False)

def Add_Random_Entry(selected_emp, employee_id, uname):
    today = date.today()
    yearmonthday = today.strftime("%Y-%m-%d")

    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Wpis")
    wnd.lift()
    wnd.attributes("-topmost", True)
    #wnd.geometry("320x332")

    topframe = Frame(wnd)
    midframe = Frame(wnd)
    dwnframe = Frame(wnd)
    dwndwnframe = Frame(wnd)

    topframe.pack(side=TOP, expand=True, fill="both")
    midframe.pack(side=TOP, expand=True, fill="both")
    dwnframe.pack(side=TOP, expand=True, fill="both")
    dwndwnframe.pack(side=TOP, expand=True, fill="both")

    lbl_date = ttk.Label(topframe, text="Wybierz datę:", font=("Arial", 13, 'bold'))
    cal = Calendar(topframe, font="Arial 15", selectmode='day', year=int(yearmonthday[0:4]),month=int(yearmonthday[5:7]),date=int(yearmonthday[8:10]))
    cal.selection_set(date(int(yearmonthday[0:4]),int(yearmonthday[5:7]),int(yearmonthday[8:10])))

    lbl_time = ttk.Label(topframe, text="Wybierz czas", font=("Arial", 13, 'bold'))

    time_picker = AnalogPicker(midframe, type=constants.HOURS24)
    time_picker.setHours(8)
    time_picker.setMinutes(0)

    action_lbl = ttk.Label(dwnframe, text="Wybierz rodzaj wpisu", font=("Arial", 11))
    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 14, 'bold'), focusthickness=3, focuscolor='none')
    s.configure("my.TMenubutton", font=('Arial', 14, 'bold'))

    holiday_dict = Create_Dict('_action', 'action')
    holiday_list = []
    reversed_dictionary = dict(map(reversed, holiday_dict.items()))
    for key in holiday_dict:
        holiday_list.append(holiday_dict[key])
    holiday_type = StringVar()
    choose_type = ttk.OptionMenu(dwnframe, holiday_type, holiday_list[0], *holiday_list, style='my.TMenubutton')

    comment=StringVar()
    lbl_comment = ttk.Label(dwndwnframe, text="Dodaj komentarz (opcjonalnie)", font=("Arial", 11))
    add_comment = ttk.Entry(dwndwnframe, textvariable=comment)

    send_button = ttk.Button(dwndwnframe, text="Dodaj wpis", style='my.TButton', command=lambda wnd=wnd, emp_id=employee_id, unam=uname: Add_Random_Entry_SQL(emp_id, cal.get_date(), reversed_dictionary[holiday_type.get()], time_picker.time(), unam, comment.get(), wnd))

    lbl_date.pack(pady=5)
    cal.pack(pady=5)
    ttk.Separator(topframe, orient='horizontal').pack(fill='x', pady=5)
    lbl_time.pack(pady=5)
    time_picker.pack(expand=True, fill="both")
    ttk.Separator(dwnframe, orient='horizontal').pack(fill='x', pady=5)
    action_lbl.pack(pady=10)
    choose_type.pack(pady=10)
    ttk.Separator(dwndwnframe, orient='horizontal').pack(fill='x', pady=5)
    lbl_comment.pack(pady=10)
    add_comment.pack(pady=10)
    send_button.pack(pady=30, ipady=10, ipadx=10)
    ttk.Label(wnd, text="Wybrany pracownik", font=("Arial", 13, 'bold')).pack(side=TOP)
    the_choosen_one = ttk.Entry(wnd, state= "disabled", font=("Arial", 13, 'bold'), justify='center', textvariable=selected_emp)
    the_choosen_one.pack(side=TOP, fill=BOTH, expan=False)

def Edit_Employee(emp_id, uname):
    if Get_Right(uname, "add_emp") == False:
        messagebox.showwarning("Ostrzeżenie", "Brak uprawnień do edycji pracowników\nSkontaktuj się z administratorem")
        return
    company_dict = Create_Dict("_firma", "firma")
    company_dict_rev = dict(map(reversed, company_dict.items()))
    company_list = []
    for key in company_dict:
        company_list.append(company_dict[key])
    dep_dict = Create_Dict("_dzial", "dzial")
    dep_dict_rev = dict(map(reversed, dep_dict.items()))
    dep_list = []
    for key in dep_dict:
        dep_list.append(dep_dict[key])
    city_dict = Create_Dict("_lokalizacja", "miasto")
    city_dict_rev = dict(map(reversed, city_dict.items()))
    city_list = []
    for key in city_dict:
        city_list.append(city_dict[key])
    tl_dict = Create_Dict("_team", "teamleader")
    tl_dict_rev = dict(map(reversed, tl_dict.items()))
    tl_list = []
    for key in tl_dict:
        tl_list.append(tl_dict[key])
    agr_dict = Create_Dict("_umowa", "rodzaj")
    agr_dict_rev = dict(map(reversed, agr_dict.items()))
    agr_list = []
    for key in agr_dict:
        agr_list.append(agr_dict[key])
    pos_dict = Create_Dict("_stanowisko", "stanowisko")
    pos_dict_rev = dict(map(reversed, pos_dict.items()))
    pos_list = []
    for key in pos_dict:
        pos_list.append(pos_dict[key])
    smk_dict = Create_Dict("_palacz", "stan")
    smk_dict_rev = dict(map(reversed, smk_dict.items()))
    smk_list = []
    for key in smk_dict:
        smk_list.append(smk_dict[key])
    emp_data = Get_Single_Emp(emp_id)[0]

    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Edytuj pracownika")
    wnd.lift()
    wnd.attributes("-topmost", True)

    maintopframe = Frame(wnd)
    maindwnframe = Frame(wnd)
    topleftframe = Frame(maintopframe)
    toprightframe = Frame(maintopframe)

    maintopframe.pack(side=TOP, expand=True, fill="both")
    entry_top = ttk.Entry(maintopframe)
    entry_top.pack(side=TOP, padx=150, pady=30)
    entry_top.insert(END, "%s %s" % (emp_data[0], emp_data[1]))
    entry_top.config(state='disabled', justify='center', font=("Arial", 15, 'bold'))
    ttk.Separator(maintopframe, orient='horizontal').pack(fill='x', pady=15)

    maindwnframe.pack(side=TOP, expand=True, fill="both")
    topleftframe.pack(side=LEFT, expand=True, fill="both")
    toprightframe.pack(side=RIGHT, expand=True, fill="both")

    

    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 12, 'bold'), focusthickness=3, focuscolor='none')
    s.configure("my.TMenubutton", font=('Arial', 12, 'bold'))

    ttk.Label(topleftframe, text="Firma", font=("Arial", 13, 'bold')).pack()
    emp_company = StringVar()
    choose_cmp = ttk.OptionMenu(topleftframe, emp_company, company_dict[emp_data[8]], *company_list, style='my.TMenubutton')
    choose_cmp.pack(pady=10)
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Dział", font=("Arial", 13, 'bold')).pack()
    emp_department = StringVar()
    choose_dep = ttk.OptionMenu(toprightframe, emp_department, dep_dict[emp_data[3]], *dep_list, style='my.TMenubutton')
    choose_dep.pack(side=TOP, pady=10)
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(topleftframe, text="Lokalizacja", font=("Arial", 13, 'bold')).pack()
    emp_city = StringVar()
    choose_city = ttk.OptionMenu(topleftframe, emp_city, city_dict[emp_data[4]], *city_list, style='my.TMenubutton')
    choose_city.pack(pady=10)
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Teamleader", font=("Arial", 13, 'bold')).pack()
    emp_tl = StringVar()
    if emp_data[5] == None:
        choose_tl = ttk.OptionMenu(toprightframe, emp_tl, tl_dict[5], *tl_list, style='my.TMenubutton')
    else:
        choose_tl = ttk.OptionMenu(toprightframe, emp_tl, tl_dict[emp_data[5]], *tl_list, style='my.TMenubutton')
    choose_tl.pack(side=TOP, pady=10)
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(topleftframe, text="Umowa", font=("Arial", 13, 'bold')).pack()
    emp_agr = StringVar()
    choose_agr = ttk.OptionMenu(topleftframe, emp_agr, agr_dict[emp_data[7]], *agr_list, style='my.TMenubutton')
    choose_agr.pack(pady=10)
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Stanowisko", font=("Arial", 13, 'bold')).pack()
    emp_pos = StringVar()
    choose_pos = ttk.OptionMenu(toprightframe, emp_pos, pos_dict[emp_data[9]], *pos_list, style='my.TMenubutton')
    choose_pos.pack(side=TOP, pady=10)
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(topleftframe, text="Palacz", font=("Arial", 13, 'bold')).pack()
    emp_smk = StringVar()
    choose_smk = ttk.OptionMenu(topleftframe, emp_smk, smk_dict[emp_data[2]], *smk_list, style='my.TMenubutton')
    choose_smk.pack(pady=10)
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Karta RFID", font=("Arial", 13, 'bold')).pack()
    entry_card = ttk.Entry(toprightframe)
    entry_card.pack(pady=10)
    entry_card.insert(END, "%s" % emp_data[6])
    entry_card.config(justify='center', font=("Arial", 13, 'bold'))
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=17)

    send_button = ttk.Button(maindwnframe, text="Edytuj pracownika", style='my.TButton', command=lambda emp_id=emp_id, wnd=wnd: Edit_Emp_Data(emp_id, company_dict_rev[emp_company.get()], dep_dict_rev[emp_department.get()], city_dict_rev[emp_city.get()], tl_dict_rev[emp_tl.get()], agr_dict_rev[emp_agr.get()], pos_dict_rev[emp_pos.get()], smk_dict_rev[emp_smk.get()], entry_card.get(), wnd))
    send_button.pack(pady=30, ipady=10, ipadx=10)

def Add_Employee(uname):
    if Get_Right(uname, "add_emp") == False:
        messagebox.showwarning("Ostrzeżenie", "Brak uprawnień do edycji pracowników\nSkontaktuj się z administratorem")
        return
    company_dict = Create_Dict("_firma", "firma")
    company_dict_rev = dict(map(reversed, company_dict.items()))
    company_list = []
    for key in company_dict:
        company_list.append(company_dict[key])
    dep_dict = Create_Dict("_dzial", "dzial")
    dep_dict_rev = dict(map(reversed, dep_dict.items()))
    dep_list = []
    for key in dep_dict:
        dep_list.append(dep_dict[key])
    city_dict = Create_Dict("_lokalizacja", "miasto")
    city_dict_rev = dict(map(reversed, city_dict.items()))
    city_list = []
    for key in city_dict:
        city_list.append(city_dict[key])
    tl_dict = Create_Dict("_team", "teamleader")
    tl_dict_rev = dict(map(reversed, tl_dict.items()))
    tl_list = []
    for key in tl_dict:
        tl_list.append(tl_dict[key])
    agr_dict = Create_Dict("_umowa", "rodzaj")
    agr_dict_rev = dict(map(reversed, agr_dict.items()))
    agr_list = []
    for key in agr_dict:
        agr_list.append(agr_dict[key])
    pos_dict = Create_Dict("_stanowisko", "stanowisko")
    pos_dict_rev = dict(map(reversed, pos_dict.items()))
    pos_list = []
    for key in pos_dict:
        pos_list.append(pos_dict[key])
    smk_dict = Create_Dict("_palacz", "stan")
    smk_dict_rev = dict(map(reversed, smk_dict.items()))
    smk_list = []
    for key in smk_dict:
        smk_list.append(smk_dict[key])

    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Dodaj pracownika")
    wnd.lift()
    wnd.attributes("-topmost", True)

    maintopframe = Frame(wnd)
    maindwnframe = Frame(wnd)
    topleftframe = Frame(maintopframe)
    toprightframe = Frame(maintopframe)

    maintopframe.pack(side=TOP, expand=True, fill="both")
    topleftframe.pack(side=LEFT, expand=True, fill="both")
    toprightframe.pack(side=RIGHT, expand=True, fill="both")
    maindwnframe.pack(side=TOP, expand=True, fill="both")

    ttk.Label(topleftframe, text="Imię", font=("Arial", 13, 'bold')).pack(pady=15)
    emp_fname = StringVar()
    maintopframe.pack(side=TOP, expand=True, fill="both")
    entry_top = ttk.Entry(topleftframe, textvariable=emp_fname)
    entry_top.pack(side=TOP, padx=60, pady=10)
    entry_top.config(justify='center', font=("Arial", 15, 'bold'))
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Nazwisko", font=("Arial", 13, 'bold')).pack(pady=15)
    emp_lname = StringVar()
    maintopframe.pack(side=TOP, expand=True, fill="both")
    entry_top = ttk.Entry(toprightframe, textvariable=emp_lname)
    entry_top.pack(side=TOP, padx=60, pady=10)
    entry_top.config(justify='center', font=("Arial", 15, 'bold'))
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=15)

    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 12, 'bold'), focusthickness=3, focuscolor='none')
    s.configure("my.TMenubutton", font=('Arial', 12, 'bold'))

    ttk.Label(topleftframe, text="Firma", font=("Arial", 13, 'bold')).pack()
    emp_company = StringVar()
    choose_cmp = ttk.OptionMenu(topleftframe, emp_company, company_list[0], *company_list, style='my.TMenubutton')
    choose_cmp.pack(pady=10)
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Dział", font=("Arial", 13, 'bold')).pack()
    emp_department = StringVar()
    choose_dep = ttk.OptionMenu(toprightframe, emp_department, dep_list[4], *dep_list, style='my.TMenubutton')
    choose_dep.pack(side=TOP, pady=10)
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(topleftframe, text="Lokalizacja", font=("Arial", 13, 'bold')).pack()
    emp_city = StringVar()
    choose_city = ttk.OptionMenu(topleftframe, emp_city, city_list[0], *city_list, style='my.TMenubutton')
    choose_city.pack(pady=10)
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Teamleader", font=("Arial", 13, 'bold')).pack()
    emp_tl = StringVar()
    choose_tl = ttk.OptionMenu(toprightframe, emp_tl, tl_list[4], *tl_list, style='my.TMenubutton')
    choose_tl.pack(side=TOP, pady=10)
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(topleftframe, text="Umowa", font=("Arial", 13, 'bold')).pack()
    emp_agr = StringVar()
    choose_agr = ttk.OptionMenu(topleftframe, emp_agr, agr_list[0], *agr_list, style='my.TMenubutton')
    choose_agr.pack(pady=10)
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Stanowisko", font=("Arial", 13, 'bold')).pack()
    emp_pos = StringVar()
    choose_pos = ttk.OptionMenu(toprightframe, emp_pos, pos_list[34], *pos_list, style='my.TMenubutton')
    choose_pos.pack(side=TOP, pady=10)
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(topleftframe, text="Palacz", font=("Arial", 13, 'bold')).pack()
    emp_smk = StringVar()
    choose_smk = ttk.OptionMenu(topleftframe, emp_smk, smk_list[0], *smk_list, style='my.TMenubutton')
    choose_smk.pack(pady=10)
    ttk.Separator(topleftframe, orient='horizontal').pack(fill='x', pady=15)

    ttk.Label(toprightframe, text="Karta RFID", font=("Arial", 13, 'bold')).pack()
    emp_card = StringVar()
    entry_card = ttk.Entry(toprightframe, textvariable=emp_card)
    entry_card.pack(pady=10)
    entry_card.config(justify='center', font=("Arial", 13, 'bold'))
    ttk.Separator(toprightframe, orient='horizontal').pack(fill='x', pady=17)

    send_button = ttk.Button(maindwnframe, text="Dodaj pracownika", style='my.TButton', command=lambda wnd=wnd: Add_Emp_SQL(emp_fname.get(), emp_lname.get(), company_dict_rev[emp_company.get()], dep_dict_rev[emp_department.get()], city_dict_rev[emp_city.get()], tl_dict_rev[emp_tl.get()], agr_dict_rev[emp_agr.get()], pos_dict_rev[emp_pos.get()], smk_dict_rev[emp_smk.get()], emp_card.get(), wnd))
    send_button.pack(pady=30, ipady=10, ipadx=10)

def Remove_Employee(emp_id, uname, frame):
    if Get_Right(uname, "rm_emp") == False:
        messagebox.showwarning("Ostrzeżenie", "Brak uprawnień do edycji pracowników\nSkontaktuj się z administratorem")
        return
    answer = askyesno(title='Usuwanie pracownika', message='Na pewno chcesz usunac pracownika?\nID: %s' % emp_id)
    if answer == True:
        Delete_Emp_SQL(emp_id)
        frame.destroy()
    else:
        print("E tam")

def Update_App(main_wnd, version, update_version):
    try:
        strtext = ""
        r = requests.get('https://p.pdaserwis.pl/pliki/update/changelog.txt', allow_redirects=True) #Get version
        strtext = str(r.content).split('_')
        strtext = strtext[0]
        strtext = strtext[2:]
        strtext = strtext.replace("\\r\\n", "\n")
    except Exception as e:
        strtext = ("Błąd pobierania listy zmian:\n %s" % e)

    def intversion(version, update_version):
        int_version = int(version[0] + version[2] + version[4:])
        int_update_version = int(update_version[0] + update_version[2] + update_version[4:])
        if int_version < int_update_version:
            return True
        else:
            return False

    if intversion(version, update_version) == False:
        messagebox.showinfo("Aktualizacja", "Wszystko jest aktualne ;)\nNowe w tej wersji:\n%s" % strtext)
        return
    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Pobieranie")
    wnd.lift()
    wnd.attributes("-topmost", True)

    prog_status=StringVar()

    def dl():
        def update_progress_bar(block_num, block_size, total_size):
            bar.config(value=block_num, maximum=block_size)
            prog_status.set(str(round(block_num/1024/1000, 2)) + " / " + str(round(block_size/1024/1000, 2)) + " MB")
            if block_num == block_size:
                messagebox.showinfo("Koniec", "Pobieranie ukończone !")
                main_wnd.quit()
                
        def wg():
            downloads_path = str(Path.home() / "Downloads") + '\\PaJer_install.exe'
            for fname in os.listdir(str(Path.home() / "Downloads")):
                if fname.startswith("PaJer_install"):
                    os.remove(os.path.join(str(Path.home() / "Downloads"), fname))
            print(downloads_path)
            wget.download('https://p.pdaserwis.pl/pliki/update/PaJer_install.exe', downloads_path, bar= update_progress_bar)
            os.startfile(downloads_path)

        dl_thread = threading.Thread(target=wg)
        dl_thread.start()

    ttk.Label(wnd, text="Pobieranie pliku", font=("Arial", 13, 'bold')).pack(pady=10)
    bar = ttk.Progressbar(wnd, length=500)
    bar.pack(pady=10, padx=20)
    prog_label = ttk.Label(wnd, textvariable=prog_status, font=("Arial", 12, 'bold'))
    prog_label.pack(pady=10)
    ttk.Label(wnd, text='Co nowego', font=("Arial", 13, 'bold')).pack(pady=10)
    changelog = ttk.Label(wnd, text=strtext)
    changelog.pack(pady=10)

    dl()

def Add_Comment(selected_emp, emp_id, uname):

    today = date.today()
    yearmonthday = today.strftime("%Y-%m-%d")

    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("Komentarz")
    wnd.lift()
    wnd.attributes("-topmost", True)

    lbl_date = ttk.Label(wnd, text="Wybierz datę:", font=("Arial", 13, 'bold'))
    cal = Calendar(wnd, font="Arial 11", selectmode='day', year=int(yearmonthday[0:4]),month=int(yearmonthday[5:7]),date=int(yearmonthday[8:10]))
    cal.selection_set(date(int(yearmonthday[0:4]),int(yearmonthday[5:7]),int(yearmonthday[8:10])))

    s = ttk.Style()
    s.configure('my.TButton', font=('Arial', 14, 'bold'), focusthickness=3, focuscolor='none')
    s.configure("my.TMenubutton", font=('Arial', 14, 'bold'))

    comment=StringVar()
    lbl_comment = ttk.Label(wnd, text="Dodaj komentarz", font=("Arial", 11))
    add_comment = ttk.Entry(wnd, textvariable=comment)

    send_button = ttk.Button(wnd, text="Dodaj wpis", style='my.TButton', command=lambda uname=uname, emp_id=emp_id, wnd=wnd: Add_Comment_SQL(emp_id.get(), cal.get_date(), uname, wnd, add_comment.get()))

    lbl_date.pack(pady=5)
    cal.pack(pady=5, padx=20)
    ttk.Separator(wnd, orient='horizontal').pack(fill='x', pady=5)
    lbl_comment.pack(pady=10)
    add_comment.pack(pady=10)
    send_button.pack(pady=30, ipady=10, ipadx=10)

    ttk.Label(wnd, text="Wybrany pracownik", font=("Arial", 13, 'bold')).pack(side=TOP)
    the_choosen_one = ttk.Entry(wnd, state= "disabled", font=("Arial", 13, 'bold'), justify='center', textvariable=selected_emp)
    the_choosen_one.pack(side=TOP, fill=BOTH, expan=False)

def ToDo():
    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("About")
    wnd.lift()
    wnd.attributes("-topmost", True)
    wnd.geometry("538x527")

    imgpath = current_directory + "\img\pink.png"
    print(imgpath)
    todo = PhotoImage(file=imgpath)

    canvas1 = Canvas(wnd)
    canvas1.pack(fill = "both", expand = True)
    canvas1.create_image(0, 0, image = todo, anchor = "nw")
    canvas1.image = todo
    ttk.Label(wnd, text="To Do!", font=("Arial", 13, 'bold')).pack()

def Edit_Employee_Overtime(emp_id, ent_id, rights_dict):
    wnd = Toplevel()
    wnd.resizable(False, False)
    wnd.iconbitmap(current_directory + "\img\\favicon.ico")
    wnd.title("About")
    wnd.lift()
    wnd.attributes("-topmost", True)

    ttk.Label(wnd, text="Podaj ilość nadgodzin:", font=("Arial", 13, 'bold')).pack(side=TOP, pady=10)
    overtime=StringVar()
    entry_overtime = ttk.Entry(wnd, textvariable=overtime)
    entry_overtime.pack(pady=10)
    entry_overtime.config(justify='center', font=("Arial", 13, 'bold'))
    
    
    send_button = ttk.Button(wnd, text="Aktualizuj", style='my.TButton', command=lambda emp_id=emp_id, ent_id=ent_id, wnd=wnd, rights_dict=rights_dict: Send_Overtime(emp_id, overtime.get(), ent_id, wnd, rights_dict))
    send_button.pack(pady=10, ipady=10, ipadx=10)
    ttk.Separator(wnd, orient='horizontal').pack(fill='x', pady=20)
    ttk.Label(wnd, text="Wybrany pracownik:", font=("Arial", 13, 'bold')).pack(side=TOP)
    ttk.Label(wnd, text=Get_Name(emp_id), font=("Arial", 13)).pack(side=TOP, pady=3)

def Month_to_String(month):
    month = int(month)
    if month == 1:
        month = "Styczeń"
    elif month == 2:
        month = "Luty"
    elif month == 3:
        month = "Marzec"
    elif month == 4:
        month = "Kwiecień"
    elif month == 5:
        month = "Maj"
    elif month == 6:
        month = "Czerwiec"
    elif month == 7:
        month = "Lipiec"
    elif month == 8:
        month = "Sierpień"
    elif month == 9:
        month = "Wrzesień"
    elif month == 10:
        month = "Październik"
    elif month == 11:
        month = "Listopad"
    elif month == 12:
        month = "Grudzień"
    return month