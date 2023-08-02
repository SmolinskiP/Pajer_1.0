import mysql.connector as database
from sql.db_connect import *
from fnct.free_days import Create_Free_days
from fnct.check_time import Check_Time
from datetime import date, datetime, timedelta
from tkinter import *
from tkinter import messagebox
import re

actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
free_days = Create_Free_days()

def Number_To_Hour(number):
    if number < 10:
        number = "0" + str(number)
    else:
        number = str(number)
    return number

def SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort):
    try:
        conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase, port = dbPort)
    except database.Error as e:
        print(f"Nie udało się połączyć z bazą danych MariaDB: {e}")
        messagebox.showerror(title="Błąd połączenia z bazą danych", message=f"Brak dostępu do bazy danych\nNajprawdopodobniej nieprawidłowe parametry połączenia\nTreść błędu:\nNie udało się połączyć z bazą danych MariaDB: {e}")
    return conn

conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)

def Get_Right(uname, right_type):
    get = conn.cursor()
    get.execute("SELECT %s FROM konta WHERE login = '%s'" % (right_type, uname))
    value = get.fetchall()[0][0]
    if value == 0:
        return False
    else:
        return True

def Create_Dict(table, name):
    dictt = {}
    get = conn.cursor()
    get.execute("SELECT id, %s FROM %s ORDER BY %s" % (name, table, name))
    value = get.fetchall()
    for key, item in value:
        dictt[key] = item
    return dictt

def Create_Emp_Dict(department, emp_dict):
    get=conn.cursor()
    query = 'SELECT id, imie, nazwisko, palacz, dzial, lokalizacja, teamleader, karta, umowa, firma, stanowisko FROM pracownicy WHERE dzial = %s AND active = 1 ORDER BY imie' % str(department)
    get.execute(query)
    value=get.fetchall()
    i=0
    temp_list = []
    for key in value:
        temp_list.append(key)
    emp_dict[department] = temp_list
    return emp_dict

def Get_Single_Emp(emp_id):
    get=conn.cursor()
    query = 'SELECT imie, nazwisko, palacz, dzial, lokalizacja, teamleader, karta, umowa, firma, stanowisko FROM pracownicy WHERE id = %s' % str(emp_id)
    get.execute(query)
    value=get.fetchall()
    print(value)
    return value

def Get_Emp_Occurance(id, date_from, date_to):
    sql_query = "SELECT id, time, action, komentarz, edit, edit_time FROM obecnosc WHERE pracownik = %s AND time > '%s' AND time < '%s 23:59:29' ORDER BY time" % (id, date_from, date_to)
    print(sql_query)
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    output = get_sql.fetchall()
    return output

def Get_Emp_List(department, rights):
    if department == 2468642:
        if rights['rm_emp'] == 0:
            messagebox.showwarning("Brak uprawnień", "Nie masz uprawnień do przeprowadzenia tej akcji\nSkontaktuj się z administratorem.")
            return
        else:
            sql_query = "SELECT id, imie, nazwisko, dzial, lokalizacja, teamleader, karta, umowa, firma, stanowisko, palacz FROM pracownicy WHERE active = 0 ORDER BY imie"
    elif rights['tl'] > 0:
        sql_query = "SELECT id, imie, nazwisko, dzial, lokalizacja, teamleader, karta, umowa, firma, stanowisko, palacz FROM pracownicy WHERE active = 1 AND teamleader = %s ORDER BY imie" % rights['tl']
    else:
        sql_query = "SELECT id, imie, nazwisko, dzial, lokalizacja, teamleader, karta, umowa, firma, stanowisko, palacz FROM pracownicy WHERE active = 1 AND dzial = %s ORDER BY imie" % department
    print(sql_query)
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    output = get_sql.fetchall()
    return output

def Delete_SQL(table, column, value):
    sql_query = "DELETE FROM %s WHERE %s = %s" % (table, column, value)
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()

def Add_Break_SQL(emp_id, date, break_start, break_end, uname, comment, window):
    comment = re.sub('\W+',' ', comment)
    actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmp_date = datetime.strptime(date, "%m/%d/%y")
    date_start = tmp_date.strftime("%Y-%m-%d") + " " + Number_To_Hour(break_start[0]) + ":" + Number_To_Hour(break_start[1]) + ":00"
    date_end = tmp_date.strftime("%Y-%m-%d") + " " + Number_To_Hour(break_end[0]) + ":" + Number_To_Hour(break_end[1]) + ":00"
    if Check_Time(break_start, break_end) == True:
        sql_query1 = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES (%s, '%s', 3, '%s', '%s', '%s')" % (emp_id, date_start, comment, uname, actual_time)
        sql_query2 = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES (%s, '%s', 4, '%s', '%s', '%s')" % (emp_id, date_end, comment, uname, actual_time)
        update_sql = conn.cursor()
        update_sql.execute(sql_query1)
        conn.commit()
        update_sql = conn.cursor()
        update_sql.execute(sql_query2)
        conn.commit()
        window.destroy()
        messagebox.showinfo(title="Sukces", message="Dodano przerwę")
    else:
        pass

def Get_Hash(uname):
    sql_query = "SELECT haslo FROM konta WHERE login = '%s'" % uname
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    output = get_sql.fetchall()[0][0]
    return output

def Change_Password_SQL(uname, hashpwd):
    sql_query = "UPDATE konta SET haslo = '%s' WHERE login = '%s'" % (hashpwd, uname)
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()

def Add_EntryExit_SQL(emp_id, date_from, date_to, time_from, time_to, uname, comment, window):
    comment = re.sub('\W+',' ', comment)
    actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dt_format = "%m/%d/%y"
    dt_date_from = datetime.strptime(date_from, dt_format)
    dt_date_to = datetime.strptime(date_to, dt_format)
    time_from = Number_To_Hour(time_from[0]) + ":" + Number_To_Hour(time_from[1]) + ":00"
    time_to = Number_To_Hour(time_to[0]) + ":" + Number_To_Hour(time_to[1]) + ":00"

    if dt_date_from > dt_date_to:
        messagebox.showwarning("Ostrzeżenie", "Data 'DO' jest mniejsza niz data 'OD'")
    elif Check_Time(time_from, time_to) == False:
        messagebox.showwarning("Ostrzeżenie", "Wyjście jest przed wejściem")
    else:
        while dt_date_from <= dt_date_to:

            date_check = dt_date_from.strftime("%Y-%m-%d")
            date_input_from = dt_date_from.strftime("%Y-%m-%d") + " " + time_from
            date_input_to = dt_date_from.strftime("%Y-%m-%d") + " " + time_to

            if date_check not in free_days:
                sql_query1 = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES (%s, '%s', 1, '%s', '%s', '%s')" % (emp_id, date_input_from, comment, uname, actual_time)
                sql_query2 = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES (%s, '%s', 2, '%s', '%s', '%s')" % (emp_id, date_input_to, comment, uname, actual_time)
                update_sql = conn.cursor()
                update_sql.execute(sql_query1)
                conn.commit()
                update_sql = conn.cursor()
                update_sql.execute(sql_query2)
                conn.commit()
            else:
                print("weekend - %s" % date_check)

            dt_date_from += timedelta(days=1)
        window.destroy()
        messagebox.showinfo(title="Sukces", message="Dodano wejście/wyjście")
def Add_EntryExit_SQL(emp_id, date_from, date_to, time_from, time_to, uname, comment, window):
    comment = re.sub('\W+',' ', comment)
    actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dt_format = "%m/%d/%y"
    dt_date_from = datetime.strptime(date_from, dt_format)
    dt_date_to = datetime.strptime(date_to, dt_format)
    time_from = Number_To_Hour(time_from[0]) + ":" + Number_To_Hour(time_from[1]) + ":00"
    time_to = Number_To_Hour(time_to[0]) + ":" + Number_To_Hour(time_to[1]) + ":00"

    if dt_date_from > dt_date_to:
        messagebox.showwarning("Ostrzeżenie", "Data 'DO' jest mniejsza niz data 'OD'")
    elif Check_Time(time_from, time_to) == False:
        messagebox.showwarning("Ostrzeżenie", "Wyjście jest przed wejściem")
    else:
        while dt_date_from <= dt_date_to:

            date_check = dt_date_from.strftime("%Y-%m-%d")
            date_input_from = dt_date_from.strftime("%Y-%m-%d") + " " + time_from
            date_input_to = dt_date_from.strftime("%Y-%m-%d") + " " + time_to

            if date_check not in free_days:
                sql_query1 = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES (%s, '%s', 1, '%s', '%s', '%s')" % (emp_id, date_input_from, comment, uname, actual_time)
                sql_query2 = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES (%s, '%s', 2, '%s', '%s', '%s')" % (emp_id, date_input_to, comment, uname, actual_time)
                update_sql = conn.cursor()
                update_sql.execute(sql_query1)
                conn.commit()
                update_sql = conn.cursor()
                update_sql.execute(sql_query2)
                conn.commit()
            else:
                print("weekend - %s" % date_check)

            dt_date_from += timedelta(days=1)
        window.destroy()
        messagebox.showinfo(title="Sukces", message="Dodano wejście/wyjście")

def Add_Holiday_SQL(emp_id, holiday_type, date_from, date_to, uname, comment, wnd):
    comment = re.sub('\W+',' ', comment)
    actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dt_format = "%m/%d/%y"
    dt_date_from = datetime.strptime(date_from, dt_format)
    dt_date_to = datetime.strptime(date_to, dt_format)
    time_str = "07:00:00"

    if dt_date_from > dt_date_to:
        print("%s jest większe niż %s" % (dt_date_from, dt_date_to))
        messagebox.showwarning("Ostrzeżenie", "Data 'DO' jest mniejsza niz data 'OD'")
    else:
        while dt_date_from <= dt_date_to:
            date_check = dt_date_from.strftime("%Y-%m-%d")
            date_input = dt_date_from.strftime("%Y-%m-%d") + " " + time_str
            if date_check not in free_days:
                sql_query = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES (%s, '%s', %s, '%s', '%s', '%s')" % (emp_id, date_input, holiday_type, comment, uname, actual_time)
                print(sql_query)
                update_sql = conn.cursor()
                update_sql.execute(sql_query)
                conn.commit()
            else:
                print("holiday")
            dt_date_from += timedelta(days=1)
        
        wnd.destroy()
        messagebox.showinfo(title="Sukces", message="Dodano urlop")

def Add_Random_Entry_SQL(emp_id, ent_date, action, ent_time, uname, comment, wnd):
    comment = re.sub('\W+',' ', comment)
    actual_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tmp_date = datetime.strptime(ent_date, "%m/%d/%y")
    ent_date = tmp_date.strftime("%Y-%m-%d") + " " + Number_To_Hour(ent_time[0]) + ":" + Number_To_Hour(ent_time[1]) + ":00"
    sql_query = "INSERT INTO obecnosc (pracownik, time, action, komentarz, edit, edit_time) VALUES (%s, '%s', %s, '%s', '%s', '%s')" % (emp_id, ent_date, action, comment, uname, actual_time)
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()
    wnd.destroy()
    messagebox.showinfo(title="Sukces", message="Dodano wpis")

def Edit_Emp_Data(emp_id, company, department, city, tl, agr, pos, smk, card, wnd):
    sql_query = "UPDATE pracownicy SET firma = %s, dzial = %s, lokalizacja = %s, teamleader = %s, umowa = %s, stanowisko = %s, palacz = %s, karta = '%s' WHERE id = %s" % (company, department, city, tl, agr, pos, smk, card, emp_id)
    try:
        int(card)
    except:
        messagebox.showwarning("Error", "Numer karty może zawierać tylko cyfry")
        return
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()
    wnd.destroy()
    messagebox.showinfo(title="Sukces", message="Zmieniono dane pracownika")

def Delete_Emp_SQL(emp_id):
    sql_query = "UPDATE pracownicy SET active = 0 WHERE id = %s" % emp_id
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()
    messagebox.showinfo(title="Sukces", message="Usunięto pracownika\n(Tak naprawdę przeniesiono do nieaktywnych, don't worry)")
    print(sql_query)

def Add_Comment_SQL(emp_id, ent_time, uname, wnd, comment):
    tmp_date = datetime.strptime(ent_time, "%m/%d/%y")
    ent_time = tmp_date.strftime("%Y-%m-%d")
    if comment == "":
        messagebox.showwarning(title="Pusty", message="Pusty komentarz\nNapisz tam coś ;)")
        return
    sql_query = "SELECT id, time FROM obecnosc WHERE pracownik = %s AND time LIKE '%s%%' ORDER BY action LIMIT 1" % (emp_id, ent_time)
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    output = get_sql.fetchall()
    try:
        comment = re.sub('\W+',' ', comment)
        sql_query = "UPDATE obecnosc SET time = '%s', komentarz = '%s' WHERE id = %s" % (output[0][1], comment, output[0][0])
        print(sql_query)
        update_sql = conn.cursor()
        update_sql.execute(sql_query)
        conn.commit()
        wnd.destroy()
        messagebox.showinfo("Komentarz", "Pomyślnie dodano komentarz")
    except Exception as e:
        messagebox.showwarning(title="404", message="Nie znaleziono żadnego wpisu dla wybranego dnia ;(\nError: %s" % e)
        return

def Activate_Employee(emp_id):
    sql_query = "UPDATE pracownicy SET active = 1 WHERE id = %s" % emp_id
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()
    messagebox.showinfo(title="Aktywny", message="Pomyślnie aktywowano pracownika")

def Add_Emp_SQL(fname, lname, cmp, dep, city, tl, agr, pos, smk, emp_card, wnd):
    if fname == "":
        messagebox.showwarning("Błąd", "Wpisz imię pracownika")
        return
    elif lname == "":
        messagebox.showwarning("Błąd", "Wpisz nazwisko pracownika")
        return
    elif emp_card == "":
        messagebox.showwarning("Błąd", "Wpisz numer karty")
        return
    try:
        int(emp_card)
    except:
        messagebox.showwarning("Błąd", "Numer karty może zawierać tylko cyfry")
        return
    sql_query = "INSERT INTO pracownicy (imie, nazwisko, firma, dzial, lokalizacja, teamleader, umowa, stanowisko, palacz, karta, active) VALUES ('%s', '%s', %s, %s, %s, %s, %s, %s, %s, '%s', 1)" % (fname, lname, cmp, dep, city, tl, agr, pos, smk, emp_card)
    print(sql_query)
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()
    wnd.destroy()
    messagebox.showinfo(title="Sukces", message="Pomyślnie dodano pracownika")

def Get_Emps_By_Department(dep, uname):
    sql_query = "SELECT id, imie, nazwisko, karta, stanowisko, dzial FROM pracownicy WHERE dzial = %s AND active = 1 ORDER BY imie" % dep
    if dep == 2468642:
        if Get_Right(uname, "rm_emp") == False:
            messagebox.showwarning("Brak uprawnień", "Nie masz uprawnień do przeprowadzenia tej akcji\nSkontaktuj się z administratorem.")
            return
        sql_query = "SELECT id, imie, nazwisko, karta, stanowisko, dzial FROM pracownicy WHERE active = 1 ORDER BY imie"
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    output = get_sql.fetchall()
    return output

def Get_Emps_By_Id(emp_id):
    sql_query = "SELECT id, imie, nazwisko, karta, stanowisko, dzial FROM pracownicy WHERE id = %s AND active = 1 ORDER BY imie" % emp_id
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    output = get_sql.fetchall()
    return output

def Get_Emps_Overtime(emp_list):
    i = 0
    new_emp_list = []
    for item in emp_list:
        sql_query = "SELECT nadgodziny, id FROM nadgodziny WHERE pracownik = %s ORDER BY data DESC LIMIT 1" % item[0]
        get_sql = conn.cursor()
        get_sql.execute(sql_query)
        output = get_sql.fetchall()[0]
        new_emp_list.append((item[0], item[1], item[2], item[3], item[4], output[0], output[1], item[5]))
    return new_emp_list

def Get_Emps_Overtime_Single(emp_list):
    i = 0
    new_emp_list = []
    for item in emp_list:
        sql_query = "SELECT nadgodziny, id, data FROM nadgodziny WHERE pracownik = %s ORDER BY data DESC" % item[0]
        get_sql = conn.cursor()
        get_sql.execute(sql_query)
        output = get_sql.fetchall()
        i=0
        for result in output:
            new_emp_list.append((item[0], item[1], item[2], item[3], item[4], result[0], result[1], item[5], result[2]))
    return new_emp_list

def Get_Name(emp_id):
    sql_query = "SELECT imie, nazwisko FROM pracownicy WHERE id = %s" % emp_id
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    output = get_sql.fetchall()
    return output[0][0] + " " + output[0][1]

def Send_Overtime(emp_id, overtime, ent_id, wnd, rights_dict):
    try:
        int(overtime)
    except:
        messagebox.showwarning("Błąd", "Ilość nadgodzin musi być liczbą")
        return
    if rights_dict['rm_emp'] == 0:
        messagebox.showwarning("Brak uprawnień", "Nie masz uprawnień do przeprowadzenia tej akcji\nSkontaktuj się z administratorem.")
        return

    sql_query = "UPDATE nadgodziny SET nadgodziny = %s WHERE id = %s" % (overtime, ent_id)
    print(sql_query)
    update_sql = conn.cursor()
    update_sql.execute(sql_query)
    conn.commit()
    wnd.destroy()
    messagebox.showinfo(title="Sukces", message="Pomyślnie zaktualizowano nadgodziny")