#import tk, ttk gui modules
from turtle import width
from tkcalendar import Calendar
from tkinter import messagebox

#import helping modules
import requests, os
import mysql.connector as database
from datetime import date, datetime

#import local modules
from login_form.login_form import *
from sql.db_data_functions import Create_Dict, Create_Emp_Dict, SQL_Connect, Get_Emp_Occurance, Get_Emp_List, Activate_Employee
from windows.rm_entry import Remove_Entry, Add_Break, Change_Password, Add_EntryExit, Add_Holiday, Add_Random_Entry, Change_Connection_Params, Edit_Employee, Remove_Employee, Changelog, Update_App, Add_Comment
from fnct.iseven import isEven
from sql.db_connect import *

version = '0.9.92'
try:
    r = requests.get('https://p.pdaserwis.pl/pliki/update/version.txt', allow_redirects=True) #Get version
    update_version = str(r.content)[2:-1]
except:
    update_version = "666"

login_form()
#RUN MAINLOOP
try:
    print(uname)
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
        e_cm = ttk.Entry(dict_firma["frame0"])
        e_cm.pack(side=LEFT)
        e_cm.insert(END, "Komentarz")
        e_cm.config(state='disabled', justify='center', font=fgfont)
        e_ed = ttk.Entry(dict_firma["frame0"])
        e_ed.pack(side=LEFT)
        e_ed.insert(END, "Edycja")
        e_ed.config(state='disabled', justify='center', font=fgfont)
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
                elif j == 3:
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
                elif j == 4:
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
                elif j == 5:
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
    e_ac = ttk.Entry(dict_firma["frame0"], width=12)
    e_ac.pack(side=LEFT)
    e_ac.insert(END, "Lokalizacja")
    e_ac.config(state='disabled', justify='center', font=fgfont)
    e_cm = ttk.Entry(dict_firma["frame0"], width=16)
    e_cm.pack(side=LEFT)
    e_cm.insert(END, "Teamleader")
    e_cm.config(state='disabled', justify='center', font=fgfont)
    e_ed = ttk.Entry(dict_firma["frame0"], width=13)
    e_ed.pack(side=LEFT)
    e_ed.insert(END, "Karta")
    e_ed.config(state='disabled', justify='center', font=fgfont)
    e_et = ttk.Entry(dict_firma["frame0"], width=15)
    e_et.pack(side=LEFT)
    e_et.insert(END, "Umowa")
    e_et.config(state='disabled', justify='center', font=fgfont)
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
            elif j == 4:
                key = "emp_city" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=12)
                e.pack(side=LEFT)
                e.insert(END, city_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 5:
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
            elif j == 6:
                key = "emp_card" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=13)
                e.pack(side=LEFT)
                e.insert(END, dict_firma[key].get())
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 7:
                key = "emp_agr" + str(i)
                dict_firma[key] = StringVar(middle_screen_panel)
                dict_firma[key].set(event[j])
                e = ttk.Entry(dict_firma["frame" + str(i)], width=15)
                e.pack(side=LEFT)
                e.insert(END, agr_dict[int(dict_firma[key].get())])
                e.config(state='disabled', justify='center', font=fgfont, foreground=fgcolor)
            elif j == 8:
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
    right_panel.pack(side=RIGHT, fill=BOTH, expand=False)
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

    cal_from = Calendar(right_panel, selectmode='day', year=int(yearmonthday[0:4]),month=int(yearmonthday[5:7]),date=int(yearmonthday[8:10]))
    cal_from.selection_set(date(int(yearmonthday[0:4]),int(yearmonthday[5:7]),int(yearmonthday[8:10])))
    cal_to = Calendar(right_panel, selectmode='day', year=int(yearmonthday[0:4]),month=int(yearmonthday[5:7]),date=int(yearmonthday[8:10]))
    cal_to.selection_set(date(int(yearmonthday[0:4]),int(yearmonthday[5:7]),int(yearmonthday[8:10])))

    ttk.Label(right_panel, text="Data OD:", font=("Arial", 13, 'bold')).pack(side=TOP)
    cal_from.pack(side=TOP)
    ttk.Separator(right_panel, orient='horizontal').pack(fill='x', pady=5)
    ttk.Label(right_panel, text="Data DO:", font=("Arial", 13, 'bold')).pack(side=TOP)
    cal_to.pack(side=TOP)
    ttk.Separator(right_panel, orient='horizontal').pack(fill='x', pady=5)
    ttk.Label(right_panel, text="Wybrany pracownik", font=("Arial", 13, 'bold')).pack(side=TOP)
    the_choosen_one = ttk.Entry(right_panel, state= "disabled", font=("Arial", 13, 'bold'), justify='center', textvariable=selected_emp)
    the_choosen_one.pack(side=TOP, fill=BOTH, expan=False)
    act_button = ttk.Button(right_panel, text='Aktualizuj\nobecność', command=lambda: Create_Table_Presence(selected_emp_id.get(), selected_emp_fname.get(), selected_emp_lname.get(), Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    act_button.pack(side=TOP, fill=BOTH, expan=False, pady=5)

    if version != update_version:
        s = ttk.Style()
        s.configure('my.TButton', font=('Arial', 16, 'bold'), focusthickness=10, focuscolor='red', background='chartreuse4')
        s.map('my.TButton', background=[('active', '#ff0000')])
        update_button = ttk.Button(right_panel, text='Dostępne aktualizacje!', style='my.TButton', command=lambda main_wnd=main_window, version=version, update_version=update_version: Update_App(main_wnd, version, update_version))
        update_button.pack(side=BOTTOM, pady=20)

    ttk.Separator(right_panel, orient='horizontal').pack(fill='x', pady=5, side=BOTTOM)
    break_btn = ttk.Button(right_panel, text='Dodaj przerwę', command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname:Add_Break(selected_emp, emp_id.get(), unam))
    break_btn.pack(side=BOTTOM, fill=BOTH, expan=False, pady=5)
    holiday_btn = ttk.Button(right_panel, text='Dodaj urlop', command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_Holiday(selected_emp, emp_id.get(), unam, Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    holiday_btn.pack(side=BOTTOM, fill=BOTH, expan=False, pady=5)
    random_btn = ttk.Button(right_panel, text='Dodaj inny wpis', command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_Random_Entry(selected_emp, emp_id.get(), unam))
    random_btn.pack(side=BOTTOM, fill=BOTH, expan=False, pady=5)
    ent_exit_btn = ttk.Button(right_panel, text='Dodaj wejście/wyjście', command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_EntryExit(selected_emp, emp_id.get(), unam, Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    ent_exit_btn.pack(side=BOTTOM, fill=BOTH, expan=False, pady=5)
    ttk.Separator(right_panel, orient='horizontal').pack(fill='x', pady=5, side=BOTTOM)

    
except:
    pass

def Create_Menu():
    emp_dict = {}
    for item in dep_dict:
        Create_Emp_Dict(item, emp_dict)
    menubar = Menu(main_window)

    opt_menu = Menu(menubar, tearoff=0)
    opt_menu.add_command(label="Opcje bazy", command=lambda: Change_Connection_Params())
    opt_menu.add_command(label="Zmien hasło", command=lambda uname=uname: Change_Password(uname))
    opt_menu.add_separator()
    opt_menu.add_command(label="Wyjście", command=lambda: main_window.quit())
    menubar.add_cascade(label="Opcje", menu=opt_menu)

    emp_menu = Menu(menubar, tearoff=0)
    emp_menu.add_command(label="Dodaj pracownika", command=donothing)
    emp_menu.add_command(label="Lista nieaktywnych", command=lambda department=2468642, rights_dict=rights_dict: Create_Table_Employees(department, rights_dict))
    dep_menu = Menu(emp_menu, tearoff=0)
    for item in rights_dict['departments']:
        dep_menu.add_command(label=dep_dict[int(item)], command=lambda department=int(item), rights_dict=rights_dict: Create_Table_Employees(department, rights_dict))
    emp_menu.add_cascade(label="Lista pracowników", menu=dep_menu)
    menubar.add_cascade(label="Pracownicy", menu=emp_menu)

    pres_menu = Menu(menubar, tearoff=0)
    empl_menu = Menu(pres_menu, tearoff=0)
    for item in rights_dict['departments']:
        new_menu = Menu(empl_menu, tearoff=0)
        empl_menu.add_cascade(label=dep_dict[int(item)], menu=new_menu)
        for x in emp_dict[int(item)]:
            new_menu.add_command(label=(x[1] + " " + x[2]), command=lambda emp_id=x[0], emp_fname=x[1], emp_lname=x[2], date_from=Get_Date_From_Callendar(cal_from), date_to=Get_Date_From_Callendar(cal_to): Create_Table_Presence(emp_id, emp_fname, emp_lname, date_from, date_to))
    add_menu = Menu(pres_menu, tearoff=0)
    add_menu.add_command(label="Dodaj przerwę", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname:Add_Break(selected_emp, emp_id.get(), unam))
    add_menu.add_command(label="Dodaj wejście/wyjście", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_EntryExit(selected_emp, emp_id.get(), unam, Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    add_menu.add_command(label="Dodaj urlop", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_Holiday(selected_emp, emp_id.get(), unam, Get_Date_From_Callendar(cal_from), Get_Date_From_Callendar(cal_to)))
    add_menu.add_command(label="Dodaj komentarz", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, uname=uname: Add_Comment(selected_emp, emp_id, uname))
    add_menu.add_command(label="Dodaj inny wpis", command=lambda selected_emp=selected_emp, emp_id=selected_emp_id, unam=uname: Add_Random_Entry(selected_emp, emp_id.get(), unam))
    pres_menu.add_cascade(label="Dodaj wpis", menu=add_menu)
    pres_menu.add_cascade(label="Lista obecności", menu=empl_menu)
    menubar.add_cascade(label="Obecnośc", menu=pres_menu)

    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="Changelog", command=lambda: Changelog())
    help_menu.add_command(label="About", command=donothing)
    help_menu.add_separator()
    help_menu.add_command(label="Aktualizacje", command=lambda main_wnd=main_window, version=version, update_version=update_version: Update_App(main_wnd, version, update_version))
    menubar.add_cascade(label="Help", menu=help_menu)

    main_window.config(menu=menubar)
    main_window.state('zoomed')
