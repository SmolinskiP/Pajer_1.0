#import tk, ttk gui modules
from turtle import width
from tkcalendar import Calendar
from tkinter import messagebox
from time import sleep
#import helping modules
import requests, os, re
import mysql.connector
import mysql.connector as database
from datetime import date, datetime

#import local modules
from login_form.login_form import *
from sql.db_data_functions import Create_Dict, Create_Emp_Dict, SQL_Connect, Get_Emp_Occurance, Get_Emp_List, Activate_Employee, Get_Emps_By_Department, Get_Emps_Overtime, Get_Emps_By_Id, Get_Emps_Overtime_Single
from windows.rm_entry import Remove_Entry, Add_Break, Change_Password, Add_EntryExit, Add_Holiday, Add_Random_Entry, Change_Connection_Params, Edit_Employee, Remove_Employee, Changelog, Update_App, Add_Comment, Add_Employee, ToDo, Edit_Employee_Overtime, Month_to_String
from fnct.iseven import isEven
from fnct.getpath import Get_Local_Path
from sql.db_connect import *
from excel_fun.presence import Create_Presence_Dict, Create_Presence_Excel

def intversion(version, update_version):
    int_version = int(version[0] + version[2] + version[4:])
    int_update_version = int(update_version[0] + update_version[2] + update_version[4:])
    if int_version < int_update_version:
        return True
    else:
        return False

try:
    conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase, port = dbPort)
except Exception as e:
    home_directory = os.path.expanduser('~')
    home_directory = os.path.join(home_directory, "Documents", "PajerApp")
    try:
        params_file_path = Get_Local_Path() + "\\sql\\params.txt"
        os.system('copy "%s" "%s"' % (params_file_path, home_directory + "\\"))
        print('copy "%s" "%s"' % (params_file_path, home_directory + "\\"))
        firstrun_check_file = open(home_directory + "\\params.txt", 'r')
        db_params = firstrun_check_file.readlines()
        firstrun_check = re.findall(r'"([^"]*)"', db_params[0])[0]
        print(firstrun_check)
        if firstrun_check != "firstrun":
            fr_file = open(home_directory + "\\firstrun.txt", 'w')
            fr_file.write("1")
            fr_file.close()
    except Exception as ex:
        print("Nie skopiowano pliku\n:%s" % ex)
    first_run = os.path.join(home_directory, "firstrun.txt")
    if os.path.isfile(first_run) == False:
    #if firstrun_check != "firstrun":
        quest_db = False
        firstrun = messagebox.askyesno(title="Błąd połączenia z bazą danych", message=f"Prawopodobnie włączasz aplikację po raz pierwszy.\n\nAby aplikacja działała jak należy, potrzebuje połączenia z bazą danych. Była testowana na bazie MariaDB, którą też polecam.\n\nWykonaj następujące kroki:\n1. Zainstaluj silnik bazy danych.\n2. Utwórz bazę danych o nazwie 'RFID' oraz użytkownika z pełnym dostępem do tej bazy\n3. Kliknij TAK, aby podać parametry połączenia\n4. Poczekaj aż zostaną utworzone niezbędne tabele i wpisy.\n5. Zresetuj aplikację i zaloguj się jako admin/qwerty\n\nhttps://mariadb.org/download/\n\n")
        if firstrun:
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

            ent_db.insert(END, "RFID")
            ent_port.insert(END, "3306")
            
            def Execute_SQL_Scripts(filename, conn):
                f = open(filename, 'r')
                sqlfile = f.read()
                f.close()
                sql_commands = sqlfile.split(';')
                c = conn.cursor()
                for command in sql_commands:
                    try:
                        print(command)
                        c.execute(command)
                    except Exception as e:
                        print("SKipped: %s" % e)

            def Params_Act(login, password, host, db, port):
                try:
                    conn = database.connect(user = login, password = password, host = host, database = db, port = port)
                    home_directory = os.path.expanduser('~')
                    home_directory = os.path.join(home_directory, "Documents", "PajerApp")
                    filepath = os.path.join(home_directory, "params.txt")
                    db_file = open(filepath, 'w')
                    db_file.write('dbLogin="%s"\n' % login)
                    db_file.write('dbPassword="%s"\n' % password)
                    db_file.write('dbHost="%s"\n' % host)
                    db_file.write('dbDatabase="%s"\n' % db)
                    db_file.write('dbPort="%s"' % port)
                    db_file.close()
                    messagebox.showinfo("Sukces", "Pomyślnie ustawiono nowe parametry połączenia\n\nAby ustawienia zadziałały, zresetuj aplikację")
                    wnd.destroy()
                    db_file = open(first_run, 'w')
                    db_file.write("1")
                    db_file.close()
                    sql_insert = messagebox.askyesno("Czy załadować SQL?", "Czy chcesz załadować skrypty SQL do utworzenia bazy danych?\nUWAGA! Nie klikaj tak, jeśli jakaś baza danych o nazwie RFID jest już stworzona.\nMoże to prowadzić do uszkodzenia bazy.")
                    if sql_insert:
                        Execute_SQL_Scripts(Get_Local_Path() + "\\DB.sql", conn)
                    sleep(5)
                    exit()
                except Exception as e:
                     messagebox.showerror("Błąd!", "Coś poszło nie tak:\n%s" % e)
        else:
            exit()
    else:
        quest_db = messagebox.askyesno(title="Błąd połączenia z bazą danych", message=f"Brak dostępu do bazy danych\nNajprawdopodobniej nieprawidłowe parametry połączenia\nTreść błędu:\nNie udało się połączyć z bazą danych MariaDB: {e}\n\nCzy chcesz podać nowe parametry połączenia?")
    if quest_db:
        Change_Connection_Params()
    else:
        pass


try:
    r = requests.get('https://p.pdaserwis.pl/pliki/update/version.txt', allow_redirects=True) #Get version
    update_version = str(r.content)[2:-1]
except:
    update_version = "0.0.1"

login_form()
#RUN MAINLOOP
try:
    tmpvariable09 = uname
    print("")
    print("==============================================================================")
    print("PaJer v%s - najlepszy program Rejestracji Czasu Pracy we wszechświecie" % version)
    print("Zalogowany użytkownik - %s" % uname)
    print("Najnowsza wersja - %s" % update_version)
    print("==============================================================================")
except:
    main_window.withdraw()
    main_window.mainloop()

def donothing():
   filewin = Toplevel(main_window)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def Get_Date_From_Callendar(callendar_name):
    str_dt = callendar_name.get_date()
    dt_format = "%m/%d/%y"
    date_obj = datetime.strptime(str_dt, dt_format)
    str_dt = date_obj.strftime("%Y-%m-%d")
    #str_dt=dt.strftime("%Y-%m-%d")
    return str_dt

def Clear(frame_name):
    for widgets in frame_name.winfo_children():
        widgets.destroy()

def Create_Table_Presence(id, fname, lname, date_from, date_to):
    date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
    date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
    if date_from_obj > date_to_obj:
        messagebox.showwarning("Ostrzeżenie", "Data 'DO' jest mniejsza niz data 'OD'")
    else:
        fgfont=('Arial', 11, 'bold')
        selected_emp.set(fname + " " + lname)
        selected_emp_id.set(id)
        selected_emp_fname.set(fname)
        selected_emp_lname.set(lname)
        Clear(middle_screen_panel)
        #conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)
        #get = conn.cursor()
        #get.execute("SELECT id, %s FROM %s" % (name, table))
        #value = get.fetchall()
        
        i = 1
        dict_firma = {}
        dict_firma["frame0"] = Frame(middle_screen_panel, highlightbackground="black", highlightthickness=0.5)
        dict_firma["frame0"].pack(anchor=NW, fill=X)
        e_lp = ttk.Entry(dict_firma["frame0"], width=5)
        e_lp.pack(side=LEFT)
        e_lp.insert(END, "LP")
        e_lp.config(state='disabled', justify='center', font=fgfont)
        e_id = ttk.Entry(dict_firma["frame0"], width=5)
        e_id.pack(side=LEFT)
        e_id.insert(END, "ID")
        e_id.config(state='disabled', justify='center', font=fgfont)
        e_fn = ttk.Entry(dict_firma["frame0"])
        e_fn.pack(side=LEFT)
        e_fn.insert(END, "Imię")
        e_fn.config(state='disabled', justify='center', font=fgfont)
        e_ln = ttk.Entry(dict_firma["frame0"])
        e_ln.pack(side=LEFT)
        e_ln.insert(END, "Nazwisko")
        e_ln.config(state='disabled', justify='center', font=fgfont)
        e_tm = ttk.Entry(dict_firma["frame0"])
        e_tm.pack(side=LEFT)
        e_tm.insert(END, "Czas")
        e_tm.config(state='disabled', justify='center', font=fgfont)
        e_ac = ttk.Entry(dict_firma["frame0"])
        e_ac.pack(side=LEFT)
        e_ac.insert(END, "Akcja")
        e_ac.config(state='disabled', justify='center', font=fgfont)
        print(main_window.winfo_width())
        if main_window.winfo_width() > 1100:
            e_cm = ttk.Entry(dict_firma["frame0"])
            e_cm.pack(side=LEFT)
            e_cm.insert(END, "Komentarz")
            e_cm.config(state='disabled', justify='center', font=fgfont)
        if main_window.winfo_width() > 1300:
            e_ed = ttk.Entry(dict_firma["frame0"])
            e_ed.pack(side=LEFT)
            e_ed.insert(END, "Edycja")
            e_ed.config(state='disabled', justify='center', font=fgfont)
        if main_window.winfo_width() > 1500:
            e_et = ttk.Entry(dict_firma["frame0"])
            e_et.pack(side=LEFT)
            e_et.insert(END, "Czas edycji")
            e_et.config(state='disabled', justify='center', font=fgfont)
        date_from = Get_Date_From_Callendar(cal_from)
        date_to = Get_Date_From_Callendar(cal_to)
        sql_result = Get_Emp_Occurance(id, date_from, date_to)
        for event in sql_result:
            if event[2] == 1:
                fgcolor="blue"
            elif event[2] == 2:
                fgcolor="DodgerBlue4"
            elif event[2] == 3:
                fgcolor="coral3"
            elif event[2] == 4:
                fgcolor="firebrick4"
            else:
                fgcolor="green"
            key = str("frame" + str(i))
            dict_firma[key] = Frame(middle_screen_panel, highlightbackground="black", highlightthickness=0.5)
            dict_firma[key].pack(anchor=N, fill=X)
            e = ttk.Entry(dict_firma["frame" + str(i)], width=5)
            e.pack(side=LEFT)
            e.insert(END, str(i))
            e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
            for j in range(len(event)):
                if j == 0:
                    key = "entry_id" + str(i)
                    dict_firma[key] = StringVar(middle_screen_panel)
                    dict_firma[key].set(event[j])
                    e = ttk.Entry(dict_firma["frame" + str(i)], width=5)
                    e.pack(side=LEFT)
                    e.insert(END, dict_firma[key].get())
                    e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
                elif j == 1:
                    e = ttk.Entry(dict_firma["frame" + str(i)])
                    e.pack(side=LEFT)
                    e.insert(END, selected_emp_fname.get())
                    e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
                    e = ttk.Entry(dict_firma["frame" + str(i)])
                    e.pack(side=LEFT)
                    e.insert(END, selected_emp_lname.get())
                    e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
                    key = "entry_time" + str(i)
                    dict_firma[key] = StringVar(middle_screen_panel)
                    dict_firma[key].set(event[j])
                    e = ttk.Entry(dict_firma["frame" + str(i)])
                    e.pack(side=LEFT)
                    e.insert(END, dict_firma[key].get())
                    e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
                elif j == 2:
                    key = "entry_action" + str(i)
                    dict_firma[key] = StringVar(middle_screen_panel)
                    dict_firma[key].set(action_dict[event[j]])
                    e = ttk.Entry(dict_firma["frame" + str(i)])
                    e.pack(side=LEFT)
                    e.insert(END, dict_firma[key].get())
                    e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
                elif j == 3 and main_window.winfo_width() > 1100:
                    key = "entry_comment" + str(i)
                    dict_firma[key] = StringVar(middle_screen_panel)
                    if event[j] == None:
                        dict_firma[key].set("")
                    else:
                        dict_firma[key].set(event[j])
                    e = ttk.Entry(dict_firma["frame" + str(i)])
                    e.pack(side=LEFT)
                    e.insert(END, dict_firma[key].get())
                    e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
                elif j == 4 and main_window.winfo_width() > 1300:
                    key = "entry_editor" + str(i)
                    dict_firma[key] = StringVar(middle_screen_panel)
                    if event[j] == None:
                        dict_firma[key].set("")
                    else:
                        dict_firma[key].set(event[j])
                    e = ttk.Entry(dict_firma["frame" + str(i)])
                    e.pack(side=LEFT)
                    e.insert(END, dict_firma[key].get())
                    e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
                elif j == 5 and main_window.winfo_width() > 1500:
                    key = "entry_edit_time" + str(i)
                    dict_firma[key] = StringVar(middle_screen_panel)
                    if event[j] == None:
                        dict_firma[key].set("")
                    else:
                        dict_firma[key].set(event[j])
                    e = ttk.Entry(dict_firma["frame" + str(i)])
                    e.pack(side=LEFT)
                    e.insert(END, dict_firma[key].get())
                    e.config(state='disabled', justify='center', foreground=fgcolor, font=fgfont)
                    rm_btn = ttk.Button(dict_firma["frame" + str(i)], text = "Usuń wpis", command=lambda uname=uname, entry_id = dict_firma["entry_id" + str(i)].get(), frame=dict_firma[str("frame" + str(i))]: Remove_Entry(entry_id, frame, uname))
                    rm_btn.pack(side=LEFT)
            i+=1
        #middle_screen.itemconfig(middle_screen_id, width=middle_screen.winfo_width())
        middle_screen.coords(middle_screen_id, middle_screen.winfo_width()/2, 0)
        main_window.update()
        middle_screen.update()
        middle_screen_panel.update()
        middle_screen.config(scrollregion=middle_screen.bbox("all"))

def Create_Table_Overtime_Emp(emp_id):
    
    Clear(middle_screen_panel)
    fgfont=('Arial', 10, 'bold')
    print(emp_id)

    i = 1
    dict_firma = {}
    dict_firma["frame0"] = Frame(middle_screen_panel, highlightbackground="black", highlightthickness=0.5)
    dict_firma["frame0"].pack(anchor=NW, fill=X)
    e_lp = ttk.Entry(dict_firma["frame0"], width=4)
    e_lp.pack(side=LEFT)
    e_lp.insert(END, "LP")
    e_lp.config(state='disabled', justify='center', font=fgfont)
    e_id = ttk.Entry(dict_firma["frame0"], width=4)
    e_id.pack(side=LEFT)
    e_id.insert(END, "ID")
    e_id.config(state='disabled', justify='center', font=fgfont)
    e_fn = ttk.Entry(dict_firma["frame0"], width=13)
    e_fn.pack(side=LEFT)
    e_fn.insert(END, "Imię")
    e_fn.config(state='disabled', justify='center', font=fgfont)
    e_ln = ttk.Entry(dict_firma["frame0"], width=13)
    e_ln.pack(side=LEFT)
    e_ln.insert(END, "Nazwisko")
    e_ln.config(state='disabled', justify='center', font=fgfont)
    if main_window.winfo_width() > 1100:
        e_tm = ttk.Entry(dict_firma["frame0"], width=20)
        e_tm.pack(side=LEFT)
        e_tm.insert(END, "Dział")
        e_tm.config(state='disabled', justify='center', font=fgfont)
    if main_window.winfo_width() > 1300:
        e_ed = ttk.Entry(dict_firma["frame0"], width=13)
        e_ed.pack(side=LEFT)
        e_ed.insert(END, "Karta")
        e_ed.config(state='disabled', justify='center', font=fgfont)
    e_et = ttk.Entry(dict_firma["frame0"], width=30)
    e_et.pack(side=LEFT)
    e_et.insert(END, "Stanowisko")
    e_et.config(state='disabled', justify='center', font=fgfont)
    e_hr = ttk.Entry(dict_firma["frame0"], width=12)
    e_hr.pack(side=LEFT)
    e_hr.insert(END, "Nadgodziny")
    e_hr.config(state='disabled', justify='center', font=fgfont)
    e_yr = ttk.Entry(dict_firma["frame0"], width=7)
    e_yr.pack(side=LEFT)
    e_yr.insert(END, "Rok")
    e_yr.config(state='disabled', justify='center', font=fgfont)
    e_mn = ttk.Entry(dict_firma["frame0"], width=11)
    e_mn.pack(side=LEFT)
    e_mn.insert(END, "Miesiąc")
    e_mn.config(state='disabled', justify='center', font=fgfont)

    emp_list = Get_Emps_By_Id(emp_id)
    emp_list = Get_Emps_Overtime_Single(emp_list)

    for event in emp_list:
        if isEven(i) == True:
            fgcolor = 'blue'
        else:
            fgcolor = 'darkblue'
        key = str("frame" + str(i))
        dict_firma[key] = Frame(middle_screen_panel, highlightbackground="black", highlightthickness=0.5)
        dict_firma[key].pack(anchor=N, fill=X)
        e = ttk.Entry(dict_firma["frame" + str(i)], width=4)
        e.pack(side=LEFT)
        e.insert(END, str(i))
        e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
        for j in range(len(event)):
            if j == 0:
                key = "emp_id" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=4)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 1:
                key = "emp_fname" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 2:
                key = "emp_lname" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 3 and main_window.winfo_width() > 1100:
                key = "emp_department" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=20)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 4 and main_window.winfo_width() > 1300:
                key = "emp_card" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j-1])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 5:
                key = "emp_pos" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j-1])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=30)
                e.pack(side=LEFT)
                e.insert(END, pos_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
                key = "emp_over" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                print(event)
                e = ttk.Entry(dict_firma["frame" + str(i)], width=12)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 6:
                key = "over_id" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
            elif j == 8:
                key = "ent_year" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=7)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get()[:4])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
                key = "ent_month" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=11)
                e.pack(side=LEFT)
                e.insert(END, Month_to_String(dict_firma[key].get()[5:7]))
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)

                edit_btn = ttk.Button(dict_firma["frame" + str(i)], text = "Edytuj", command=lambda emp_id = dict_firma["emp_id" + str(i)].get(), ent_id = dict_firma["over_id" + str(i)].get(), rights_dict=rights_dict: Edit_Employee_Overtime(emp_id, ent_id, rights_dict))
                edit_btn.pack(side=LEFT)
        i+=1
    middle_screen.coords(middle_screen_id, middle_screen.winfo_width()/2, 0)
    main_window.update()
    middle_screen.update()
    middle_screen_panel.update()
    middle_screen.config(scrollregion=middle_screen.bbox("all"))

def Create_Table_Overtime_Dep(department):
    
    Clear(middle_screen_panel)
    fgfont=('Arial', 10, 'bold')
    print(department)

    i = 1
    dict_firma = {}
    dict_firma["frame0"] = Frame(middle_screen_panel, highlightbackground="black", highlightthickness=0.5)
    dict_firma["frame0"].pack(anchor=NW, fill=X)
    e_lp = ttk.Entry(dict_firma["frame0"], width=4)
    e_lp.pack(side=LEFT)
    e_lp.insert(END, "LP")
    e_lp.config(state='disabled', justify='center', font=fgfont)
    e_id = ttk.Entry(dict_firma["frame0"], width=4)
    e_id.pack(side=LEFT)
    e_id.insert(END, "ID")
    e_id.config(state='disabled', justify='center', font=fgfont)
    e_fn = ttk.Entry(dict_firma["frame0"], width=13)
    e_fn.pack(side=LEFT)
    e_fn.insert(END, "Imię")
    e_fn.config(state='disabled', justify='center', font=fgfont)
    e_ln = ttk.Entry(dict_firma["frame0"], width=13)
    e_ln.pack(side=LEFT)
    e_ln.insert(END, "Nazwisko")
    e_ln.config(state='disabled', justify='center', font=fgfont)
    e_tm = ttk.Entry(dict_firma["frame0"], width=20)
    e_tm.pack(side=LEFT)
    e_tm.insert(END, "Dział")
    e_tm.config(state='disabled', justify='center', font=fgfont)
    e_ed = ttk.Entry(dict_firma["frame0"], width=13)
    e_ed.pack(side=LEFT)
    e_ed.insert(END, "Karta")
    e_ed.config(state='disabled', justify='center', font=fgfont)
    e_et = ttk.Entry(dict_firma["frame0"], width=30)
    e_et.pack(side=LEFT)
    e_et.insert(END, "Stanowisko")
    e_et.config(state='disabled', justify='center', font=fgfont)
    e_hr = ttk.Entry(dict_firma["frame0"], width=12)
    e_hr.pack(side=LEFT)
    e_hr.insert(END, "Nadgodziny")
    e_hr.config(state='disabled', justify='center', font=fgfont)

    emp_list = Get_Emps_By_Department(department, uname, rights_dict)
    emp_list = Get_Emps_Overtime(emp_list)

    for event in emp_list:
        if isEven(i) == True:
            fgcolor = 'blue'
        else:
            fgcolor = 'darkblue'
        key = str("frame" + str(i))
        dict_firma[key] = Frame(middle_screen_panel, highlightbackground="black", highlightthickness=0.5)
        dict_firma[key].pack(anchor=N, fill=X)
        e = ttk.Entry(dict_firma["frame" + str(i)], width=4)
        e.pack(side=LEFT)
        e.insert(END, str(i))
        e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
        for j in range(len(event)):
            if j == 0:
                key = "emp_id" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=4)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 1:
                key = "emp_fname" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 2:
                key = "emp_lname" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 3:
                key = "emp_department" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j+4])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=20)
                e.pack(side=LEFT)
                e.insert(END, dep_dict[event[j+4]])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 4:
                key = "emp_card" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j-1])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 5:
                key = "emp_pos" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j-1])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=30)
                e.pack(side=LEFT)
                e.insert(END, pos_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
                key = "emp_over" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=12)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 6:
                key = "over_id" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])

                edit_btn = ttk.Button(dict_firma["frame" + str(i)], text = "Edytuj", command=lambda emp_id = dict_firma["emp_id" + str(i)].get(), ent_id = dict_firma["over_id" + str(i)].get(), rights_dict=rights_dict: Edit_Employee_Overtime(emp_id, ent_id, rights_dict))
                edit_btn.pack(side=LEFT)
        i+=1
    middle_screen.coords(middle_screen_id, middle_screen.winfo_width()/2, 0)
    main_window.update()
    middle_screen.update()
    middle_screen_panel.update()
    middle_screen.config(scrollregion=middle_screen.bbox("all"))

def Create_Table_Employees(department, rights_dict):

    Clear(middle_screen_panel)
    fgfont=('Arial', 10, 'bold')
    print(department)

    i = 1
    dict_firma = {}
    dict_firma["frame0"] = Frame(middle_screen_panel, highlightbackground="black", highlightthickness=0.5)
    dict_firma["frame0"].pack(anchor=NW, fill=X)
    e_lp = ttk.Entry(dict_firma["frame0"], width=4)
    e_lp.pack(side=LEFT)
    e_lp.insert(END, "LP")
    e_lp.config(state='disabled', justify='center', font=fgfont)
    e_id = ttk.Entry(dict_firma["frame0"], width=4)
    e_id.pack(side=LEFT)
    e_id.insert(END, "ID")
    e_id.config(state='disabled', justify='center', font=fgfont)
    e_fn = ttk.Entry(dict_firma["frame0"], width=13)
    e_fn.pack(side=LEFT)
    e_fn.insert(END, "Imię")
    e_fn.config(state='disabled', justify='center', font=fgfont)
    e_ln = ttk.Entry(dict_firma["frame0"], width=13)
    e_ln.pack(side=LEFT)
    e_ln.insert(END, "Nazwisko")
    e_ln.config(state='disabled', justify='center', font=fgfont)
    e_tm = ttk.Entry(dict_firma["frame0"])
    e_tm.pack(side=LEFT)
    e_tm.insert(END, "Dział")
    e_tm.config(state='disabled', justify='center', font=fgfont)
    if main_window.winfo_width() > 1500:
        e_ac = ttk.Entry(dict_firma["frame0"], width=12)
        e_ac.pack(side=LEFT)
        e_ac.insert(END, "Lokalizacja")
        e_ac.config(state='disabled', justify='center', font=fgfont)
    if main_window.winfo_width() > 1300:
        e_cm = ttk.Entry(dict_firma["frame0"], width=16)
        e_cm.pack(side=LEFT)
        e_cm.insert(END, "Teamleader")
        e_cm.config(state='disabled', justify='center', font=fgfont)
    if main_window.winfo_width() > 1100:
        e_ed = ttk.Entry(dict_firma["frame0"], width=13)
        e_ed.pack(side=LEFT)
        e_ed.insert(END, "Karta")
        e_ed.config(state='disabled', justify='center', font=fgfont)
    if main_window.winfo_width() > 900:
        e_et = ttk.Entry(dict_firma["frame0"], width=15)
        e_et.pack(side=LEFT)
        e_et.insert(END, "Umowa")
        e_et.config(state='disabled', justify='center', font=fgfont)
    if main_window.winfo_width() > 700:
        e_et = ttk.Entry(dict_firma["frame0"])
        e_et.pack(side=LEFT)
        e_et.insert(END, "Firma")
        e_et.config(state='disabled', justify='center', font=fgfont)
    e_et = ttk.Entry(dict_firma["frame0"])
    e_et.pack(side=LEFT)
    e_et.insert(END, "Stanowisko")
    e_et.config(state='disabled', justify='center', font=fgfont)
    e_et = ttk.Entry(dict_firma["frame0"])
    e_et.pack(side=LEFT)
    e_et.insert(END, "Palacz")
    e_et.config(state='disabled', justify='center', font=fgfont, width='7')

    sql_result = Get_Emp_List(department, rights_dict)

    for event in sql_result:
        if isEven(i) == True:
            fgcolor = 'blue'
        else:
            fgcolor = 'darkblue'
        key = str("frame" + str(i))
        dict_firma[key] = Frame(middle_screen_panel, highlightbackground="black", highlightthickness=0.5)
        dict_firma[key].pack(anchor=N, fill=X)
        e = ttk.Entry(dict_firma["frame" + str(i)], width=4)
        e.pack(side=LEFT)
        e.insert(END, str(i))
        e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
        for j in range(len(event)):
            if j == 0:
                key = "emp_id" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=4)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 1:
                key = "emp_fname" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 2:
                key = "emp_lname" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 3:
                key = "emp_department" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)])
                e.pack(side=LEFT)
                e.insert(END, dep_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 4 and main_window.winfo_width() > 1500:
                key = "emp_city" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=12)
                e.pack(side=LEFT)
                e.insert(END, city_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 5 and main_window.winfo_width() > 1300:
                key = "emp_tl" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=16)
                e.pack(side=LEFT)
                try:
                    e.insert(END, tl_dict[int(dict_firma[key].get())])
                except:
                    e.insert(END, "Nie dotyczy")
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 6 and main_window.winfo_width() > 1100:
                key = "emp_card" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 7 and main_window.winfo_width() > 900:
                key = "emp_agr" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=15)
                e.pack(side=LEFT)
                e.insert(END, agr_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 8 and main_window.winfo_width() > 700:
                key = "emp_cmp" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)])
                e.pack(side=LEFT)
                e.insert(END, company_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 9:
                key = "emp_pos" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)])
                e.pack(side=LEFT)
                e.insert(END, pos_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 10:
                key = "emp_smk" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)])
                e.pack(side=LEFT)
                e.insert(END, smk_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor, width='7')
                if department == 2468642:
                    activate_btn = ttk.Button(dict_firma["frame" + str(i)], text = "Aktywuj", command=lambda emp_id = dict_firma["emp_id" + str(i)].get(): Activate_Employee(emp_id))
                    activate_btn.pack(side=LEFT)
                else:
                    edit_btn = ttk.Button(dict_firma["frame" + str(i)], text = "Edytuj dane", command=lambda uname=uname, emp_id = dict_firma["emp_id" + str(i)].get(): Edit_Employee(emp_id, uname))
                    edit_btn.pack(side=LEFT)
                    rm_btn = ttk.Button(dict_firma["frame" + str(i)], text = "Usuń", width = 5, command=lambda uname=uname, emp_id = dict_firma["emp_id" + str(i)].get(), frame=dict_firma[str("frame" + str(i))]: Remove_Employee(emp_id, uname, frame))
                    rm_btn.pack(side=LEFT)
                choose_btn = ttk.Button(dict_firma["frame" + str(i)], text = "Wybierz", command=lambda emp_id=dict_firma["emp_id" + str(i)].get(), emp_fname=dict_firma["emp_fname" + str(i)].get(), emp_lname=dict_firma["emp_lname" + str(i)].get(), date_from=Get_Date_From_Callendar(cal_from), date_to=Get_Date_From_Callendar(cal_to): Create_Table_Presence(emp_id, emp_fname, emp_lname, date_from, date_to))
                choose_btn.pack(side=LEFT)
        i+=1

    middle_screen.coords(middle_screen_id, middle_screen.winfo_width()/2, 0)
    main_window.update()
    middle_screen.update()
    middle_screen_panel.update()
    middle_screen.config(scrollregion=middle_screen.bbox("all"))


today = date.today()
yearmonthday = today.strftime("%Y-%m-%d")

global time_from
global time_to
global selected_emp
global selected_emp_id
global selected_emp_fname
global selected_emp_lname
global right_panel_message
global action_dict 
action_dict = Create_Dict("_action", "action")

company_dict = Create_Dict("_firma", "firma")
company_list = []
for key in company_dict:
    company_list.append(company_dict[key])

dep_dict = Create_Dict("_dzial", "dzial")
dep_list = []
for key in dep_dict:
    dep_list.append(dep_dict[key])

city_dict = Create_Dict("_lokalizacja", "miasto")
city_list = []
for key in city_dict:
    city_list.append(city_dict[key])

tl_dict = Create_Dict("_team", "teamleader")
tl_list = []
for key in tl_dict:
    tl_list.append(tl_dict[key])

agr_dict = Create_Dict("_umowa", "rodzaj")
agr_list = []
for key in agr_dict:
    agr_list.append(agr_dict[key])

pos_dict = Create_Dict("_stanowisko", "stanowisko")
pos_list = []
for key in pos_dict:
    pos_list.append(pos_dict[key])

smk_dict = Create_Dict("_palacz", "stan")
smk_list = []
for key in smk_dict:
    smk_list.append(smk_dict[key])


try:
    time_from=StringVar()
    time_to=StringVar()
    selected_emp=StringVar()
    selected_emp_id=StringVar()
    selected_emp_fname=StringVar()
    selected_emp_lname=StringVar()
    right_panel_message=StringVar()
    selected_emp.set("Wybierz pracownika")

    scrollframe = Frame(main_window)
    right_panel = Frame(main_window)
    
    right_panel.pack(side=BOTTOM, fill=BOTH, expand=False)
    ttk.Separator(right_panel, orient='horizontal').pack(fill='x', pady=5, side=TOP)
    ttk.Separator(right_panel, orient='horizontal').pack(fill='x', pady=5, side=BOTTOM)
    cal_from_panel = Frame(right_panel)
    cal_from_panel.pack(side=LEFT, fill=BOTH, expand=False, padx=5, ipadx=5)
    
    
    cal_to_panel = Frame(right_panel)
    cal_to_panel.pack(side=LEFT, fill=BOTH, expand=False, padx=5, ipadx=5)
    current_employee_panel = Frame(right_panel)
    current_employee_panel.pack(side=LEFT, fill=BOTH, expand=False)
    
    random_buttons_panel = Frame(right_panel)
    random_buttons_panel.pack(side=RIGHT, expand=False)
    actualization_button_panel = Frame(right_panel)
    actualization_button_panel.pack(side=RIGHT, fill=BOTH, expand=False)
    
    scrollframe.pack(side=LEFT, fill=BOTH, expand=True)
    vscrollbar = Scrollbar(scrollframe, orient='vertical')
    middle_screen = Canvas(scrollframe, yscrollcommand=vscrollbar.set)
    vscrollbar.config(command=middle_screen.yview)
    vscrollbar.pack(side=RIGHT, fill=Y)
    middle_screen_panel = Frame(middle_screen, bg='red')
    middle_screen.pack(side=TOP, fill=BOTH, expand=True)
    middle_screen_id = middle_screen.create_window(middle_screen.winfo_width()/2,middle_screen.winfo_width()/2,window=middle_screen_panel, anchor='n', tags="frame")
    main_window.update()
    middle_screen.update()
    middle_screen_panel.update()
    middle_screen.config(scrollregion=middle_screen.bbox("all"))

    conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)
    get = conn.cursor()
    get.execute("SELECT id_baza FROM konta WHERE login = '%s'" % uname)
    uname_id = get.fetchall()[0][0]
    get.execute("SELECT imie, nazwisko, dzial FROM pracownicy WHERE id = '%s'" % uname_id)
    uname_value = get.fetchall()
    uname_fname = uname_value[0][0]
    uname_lname = uname_value[0][1]
    uname_dep = uname_value[0][2]
    selected_emp.set(uname_fname + " " + uname_lname)
    selected_emp_id.set(uname_id)
    selected_emp_fname.set(uname_fname)
    selected_emp_lname.set(uname_lname)

    cal_from = Calendar(cal_from_panel, selectmode='day', year=int(yearmonthday[0:4]),month=int(yearmonthday[5:7]),date=int(yearmonthday[8:10]))
    cal_from.selection_set(date(int(yearmonthday[0:4]),int(yearmonthday[5:7]),int(yearmonthday[8:10])))
    cal_to = Calendar(cal_to_panel, selectmode='day', year=int(yearmonthday[0:4]),month=int(yearmonthday[5:7]),date=int(yearmonthday[8:10]))
    cal_to.selection_set(date(int(yearmonthday[0:4]),int(yearmonthday[5:7]),int(yearmonthday[8:10])))

    ttk.Label(cal_from_panel, text="Excel / Data OD:", font=("Arial", 13, 'bold')).pack(side=TOP)
    cal_from.pack(side=TOP)
    
    ttk.Label(cal_to_panel, text="Data DO:", font=("Arial", 13, 'bold')).pack(side=TOP)
    cal_to.pack(side=TOP, ipadx=5)
    #ttk.Separator(right_panel, orient='horizontal').pack(fill='x', padx=5)
    ttk.Separator(current_employee_panel, orient='horizontal').pack(fill='x', pady=5, side=BOTTOM)
    ttk.Label(current_employee_panel, text="Wybrany pracownik", font=("Arial", 13, 'bold')).pack(side=BOTTOM)
    the_choosen_one = ttk.Entry(current_employee_panel, state= "disabled", font=("Arial", 13, 'bold'), justify='center', textvariable=selected_emp)
    the_choosen_one.pack(side=BOTTOM, fill=BOTH, expan=False)
    ttk.Separator(current_employee_panel, orient='horizontal').pack(fill='x', pady=5, side=BOTTOM)
    act_button = ttk.Button(current_employee_panel, text='Aktualizuj\nobecność', command=lambda: Create_Table_Presence(selected_emp_id.get(), selected_emp_fname.get(), selected_emp_lname.get(), Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    act_button.pack(side=BOTTOM, fill=BOTH, expan=False, pady=5)
    exc_button = ttk.Button(current_employee_panel, text='                 Szybki Excel\n  (Aktualnie wybrany pracownik)', command=lambda: Create_Presence_Excel(Create_Presence_Dict(connection_dict, conn, int(Get_Date_From_Callendar(cal_from)[:4]), int(Get_Date_From_Callendar(cal_from)[5:7]), employee=selected_emp_id.get()), int(Get_Date_From_Callendar(cal_from)[:4]), int(Get_Date_From_Callendar(cal_from)[5:7]), smk_dict, action_dict, dep_dict, company_dict, city_dict, agr_dict, pos_dict))
    ttk.Separator(current_employee_panel, orient='horizontal').pack(fill='x', pady=5, side=BOTTOM)
    exc_button.pack(side=BOTTOM, fill=BOTH, expan=False, pady=8)
    
    
    if intversion(version, update_version) == True:
        s = ttk.Style()
        s.configure('my.TButton', font=('Arial', 16, 'bold'), focusthickness=10, focuscolor='red', background='chartreuse4')
        s.map('my.TButton', background=[('active', '#ff0000')])
        update_button = ttk.Button(right_panel, text='Dostępne aktualizacje!', style='my.TButton', command=lambda main_wnd=main_window, version=version, update_version=update_version: Update_App(main_wnd, version, update_version))
        update_button.pack(side=BOTTOM, pady=30, padx=60, fill=BOTH, expand=True)
    else:
        imgpath_pda = current_directory + "\img\logo.png"
        logo_pda = PhotoImage(file=imgpath_pda)
        actualization_label = Label(right_panel, image = logo_pda)
        actualization_label.pack(fill=X, pady=50)

    ttk.Separator(random_buttons_panel, orient='horizontal').pack(fill='x', pady=5, side=BOTTOM)
    break_btn = ttk.Button(random_buttons_panel, text='Dodaj przerwę', command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname:Add_Break(selected_emp, emp_id.get(), unam))
    break_btn.pack(side=BOTTOM, fill=BOTH, expan=False, pady=7, ipadx=20)
    holiday_btn = ttk.Button(random_buttons_panel, text='Dodaj urlop', command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_Holiday(selected_emp, emp_id.get(), unam, Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    holiday_btn.pack(side=BOTTOM, fill=BOTH, expan=False, pady=7)
    random_btn = ttk.Button(random_buttons_panel, text='Dodaj inny wpis', command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_Random_Entry(selected_emp, emp_id.get(), unam))
    random_btn.pack(side=BOTTOM, fill=BOTH, expan=False, pady=7)
    ent_exit_btn = ttk.Button(random_buttons_panel, text='Dodaj wejście/wyjście', command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_EntryExit(selected_emp, emp_id.get(), unam, Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    ent_exit_btn.pack(side=BOTTOM, fill=BOTH, expan=False, pady=7, ipadx=70)
    ttk.Separator(random_buttons_panel, orient='horizontal').pack(fill='x', pady=5, side=BOTTOM)
    
    
except:
    pass

def Create_Menu():
    emp_dict = {}
    for item in dep_dict:
        Create_Emp_Dict(item, emp_dict, rights_dict)
    menubar = Menu(main_window)

    opt_menu = Menu(menubar, tearoff=0)
    opt_menu.add_command(label="Opcje bazy", command=lambda: Change_Connection_Params())
    opt_menu.add_command(label="Zmien hasło", command=lambda uname=uname: Change_Password(uname))
    opt_menu.add_separator()
    opt_menu.add_command(label="Wyjście", command=lambda: main_window.quit())
    menubar.add_cascade(label="Opcje", menu=opt_menu)

    emp_menu = Menu(menubar, tearoff=0)
    emp_menu.add_command(label="Dodaj pracownika", command=lambda: Add_Employee(uname))
    emp_menu.add_command(label="Lista nieaktywnych", command=lambda department=2468642, rights_dict=rights_dict: Create_Table_Employees(department, rights_dict))
    dep_menu = Menu(emp_menu, tearoff=0)
    for item in rights_dict['departments']:
        dep_menu.add_command(label=dep_dict[int(item)], command=lambda department=int(item), rights_dict=rights_dict: Create_Table_Employees(department, rights_dict))
    emp_menu.add_cascade(label="Lista pracowników", menu=dep_menu)
    menubar.add_cascade(label="Pracownicy", menu=emp_menu)

    empl_menu = Menu(emp_menu, tearoff=0)
    for item in rights_dict['departments']:
        new_menu = Menu(empl_menu, tearoff=0)
        empl_menu.add_cascade(label=dep_dict[int(item)], menu=new_menu)
        for x in emp_dict[int(item)]:
            new_menu.add_command(label=(x[1] + " " + x[2]), command=lambda emp_id=x[0], emp_fname=x[1], emp_lname=x[2], date_from=Get_Date_From_Callendar(cal_from), date_to=Get_Date_From_Callendar(cal_to): Create_Table_Presence(emp_id, emp_fname, emp_lname, date_from, date_to))
    emp_menu.add_cascade(label="Lista obecności", menu=empl_menu)

    pres_menu = Menu(menubar, tearoff=0)
    pres_menu.add_command(label="Dodaj przerwę", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname:Add_Break(selected_emp, emp_id.get(), unam))
    pres_menu.add_command(label="Dodaj wejście/wyjście", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_EntryExit(selected_emp, emp_id.get(), unam, Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    pres_menu.add_command(label="Dodaj urlop", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_Holiday(selected_emp, emp_id.get(), unam, Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    pres_menu.add_command(label="Dodaj komentarz", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, uname=uname: Add_Comment(selected_emp, emp_id, uname))
    pres_menu.add_command(label="Dodaj inny wpis", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_Random_Entry(selected_emp, emp_id.get(), unam))
    menubar.add_cascade(label="Wpisy", menu=pres_menu)

    overtime_menu = Menu(menubar, tearoff=0)
    ov_dep_menu = Menu(overtime_menu, tearoff=0)
    for item in rights_dict['departments']:
        ov_dep_menu.add_command(label=dep_dict[int(item)], command=lambda department=int(item): Create_Table_Overtime_Dep(department))
    overtime_menu.add_cascade(label="Dział", menu=ov_dep_menu)
    menubar.add_cascade(label="Nadgodziny", menu=overtime_menu)

    ov_emp_menu = Menu(overtime_menu, tearoff=0)
    for item in rights_dict['departments']:
        new_menu = Menu(ov_emp_menu, tearoff=0)
        ov_emp_menu.add_cascade(label=dep_dict[int(item)], menu=new_menu)
        for x in emp_dict[int(item)]:
            new_menu.add_command(label=(x[1] + " " + x[2]), command=lambda emp_id=x[0]:Create_Table_Overtime_Emp(emp_id))
    overtime_menu.add_cascade(label="Pracownik", menu=ov_emp_menu)
    overtime_menu.add_command(label="Wszyscy", command=lambda: Create_Table_Overtime_Dep(2468642))
    
    excel_menu = Menu(menubar, tearoff=0)
    for item in rights_dict['departments']:
        excel_menu.add_command(label=dep_dict[int(item)], command=lambda department=int(item), conn=conn: Create_Presence_Excel(Create_Presence_Dict(connection_dict, conn, int(Get_Date_From_Callendar(cal_from)[:4]), int(Get_Date_From_Callendar(cal_from)[5:7]), department=department), int(Get_Date_From_Callendar(cal_from)[:4]), int(Get_Date_From_Callendar(cal_from)[5:7]), smk_dict, action_dict, dep_dict, company_dict, city_dict, agr_dict, pos_dict))
    if rights_dict['uprawnienia'] == 777:
        excel_menu.add_command(label="PŁOŃSK", command=lambda conn=conn: Create_Presence_Excel(Create_Presence_Dict(connection_dict, conn, int(Get_Date_From_Callendar(cal_from)[:4]), int(Get_Date_From_Callendar(cal_from)[5:7]), localization=1), int(Get_Date_From_Callendar(cal_from)[:4]), int(Get_Date_From_Callendar(cal_from)[5:7]), smk_dict, action_dict, dep_dict, company_dict, city_dict, agr_dict, pos_dict))
        excel_menu.add_command(label="WARSZAWA", command=lambda conn=conn: Create_Presence_Excel(Create_Presence_Dict(connection_dict, conn, int(Get_Date_From_Callendar(cal_from)[:4]), int(Get_Date_From_Callendar(cal_from)[5:7]), localization=2), int(Get_Date_From_Callendar(cal_from)[:4]), int(Get_Date_From_Callendar(cal_from)[5:7]), smk_dict, action_dict, dep_dict, company_dict, city_dict, agr_dict, pos_dict))
    menubar.add_cascade(label="Excel", menu=excel_menu)

    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="Changelog", command=lambda: Changelog())
    help_menu.add_command(label="About", command=lambda: ToDo())
    help_menu.add_separator()
    help_menu.add_command(label="Aktualizacje", command=lambda main_wnd=main_window, version=version, update_version=update_version: Update_App(main_wnd, version, update_version))
    menubar.add_cascade(label="Help", menu=help_menu)

    main_window.config(menu=menubar)
    main_window.state('zoomed')
    