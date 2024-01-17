import mysql.connector as database
import xlsxwriter, calendar
from fnct.free_days import Create_Free_days
from excel_fun.random_fun import Number_to_String, Generate_Overtime, Expected_Time, Month_to_String, Cell_Type_Entry_Exit
from time import strftime
import os, math
from datetime import datetime, timedelta


def Create_Presence_Dict(connection_dict, conn, year, month, localization=0, department=0, employee=0):
    print(connection_dict)
    print("Generuję plik Excel do: %s" % os.path.join(os.path.expanduser('~'), "Documents", ""))
    print("Parametry pliku:\nRok: %s\nMiesiąc: %s\nLokalizacja: %s\nDział: %s\nPracownik: %s\n" % (year, month, localization, department, employee))
    conn = database.connect(user = connection_dict['login'], password = connection_dict['password'], host = connection_dict['host'], database = connection_dict['db'], port = connection_dict['port'])
    get_sql = conn.cursor()
    employee_dict = {}
    
    if localization != 0:
        sql_query = "SELECT id, imie, nazwisko, palacz, dzial, umowa, firma, stanowisko FROM pracownicy WHERE active = 1 AND lokalizacja = %s ORDER BY nazwisko" % localization
        get_sql.execute(sql_query)
        sql_result = get_sql.fetchall()
        for item in sql_result:
            employee_dict[item[0]] = [item[1], item[2], item[3], localization, item[4], item[5], item[6], item[7], [], [], []]
    elif department != 0:
        sql_query = "SELECT id, imie, nazwisko, palacz, lokalizacja, umowa, firma, stanowisko FROM pracownicy WHERE active = 1 AND dzial = %s ORDER BY nazwisko" % department
        get_sql.execute(sql_query)
        sql_result = get_sql.fetchall()
        for item in sql_result:
            employee_dict[item[0]] = [item[1], item[2], item[3], item[4], department, item[5], item[6], item[7], [], [], []]
    elif employee != 0:
        sql_query = "SELECT id, imie, nazwisko, palacz, lokalizacja, dzial, umowa, firma, stanowisko FROM pracownicy WHERE active = 1 AND id = %s" % employee
        get_sql.execute(sql_query)
        sql_result = get_sql.fetchall()
        for item in sql_result:
            employee_dict[item[0]] = [item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], [], [], []]
        
    sql_query = "SELECT pracownik, action, time , komentarz FROM obecnosc WHERE pracownik IN ("
    for key, item in employee_dict.items():
        sql_query += "%s, " % key
    sql_query = sql_query[:-2]
    if month < 10:
        month = "0" + str(month)
    sql_query += ") AND TIME LIKE '%s%%' ORDER BY pracownik, time" % (str(year) + "-" + str(month))
    get_sql.execute(sql_query)
    sql_result = get_sql.fetchall()

    for item in sql_result:
        for key, value in employee_dict.items():
            if item[0] == key:
                employee_dict[key][8].append(item)
    
                
    sql_query = "SELECT pracownik, nadgodziny FROM nadgodziny WHERE pracownik IN ("
    for key, item in employee_dict.items():
        sql_query += "%s, " % key
    sql_query = sql_query[:-2]
    month = int(month)
    if month < 10:
        month = "0" + str(month)
    sql_query += ") AND data LIKE '%s%%' ORDER BY pracownik, data" % (str(year) + "-" + str(month))
    print(sql_query)
    get_sql.execute(sql_query)
    sql_result = get_sql.fetchall()

    for item in sql_result:
        for key, value in employee_dict.items():
            if item[0] == key:
                employee_dict[key][10].append(item)
                
    sql_query = "SELECT pracownik, nadgodziny FROM nadgodziny WHERE pracownik IN ("
    for key, item in employee_dict.items():
        sql_query += "%s, " % key
    sql_query = sql_query[:-2]
    month = int(month)
    if month == 1:
        year-=1
    else:
        month-=1
    if month < 10:
        month = "0" + str(month)
    sql_query += ") AND data LIKE '%s%%' ORDER BY pracownik, data" % (str(year) + "-" + str(month))
    get_sql.execute(sql_query)
    sql_result = get_sql.fetchall()

    for item in sql_result:
        for key, value in employee_dict.items():
            if item[0] == key:
                employee_dict[key][9].append(item)
                
        
    return employee_dict

def Create_Presence_Excel(pres_dict, year, month, smk_dict, action_dict, dep_dict, company_dict, city_dict, agr_dict, pos_dict, just_worker=0, just_department=0):
    #print(pres_dict)
    if just_worker == 0 and just_department == 0:
        workbook = xlsxwriter.Workbook(os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc.xlsm"))
    elif just_department != 0:
        workbook = xlsxwriter.Workbook(os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc_dep_%s.xlsm" % just_department))
    else:
        workbook = xlsxwriter.Workbook(os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc_%s.xlsm" % list(pres_dict.keys())[0]))
    print(dep_dict)
    red_cell = workbook.add_format({'font_color': 'white', 'bg_color': 'red', 'bold': True})
    red_time_cell = workbook.add_format({'font_color': 'white', 'bg_color': 'red', 'bold': True, 'num_format': 'hh:mm:ss'})
    orange_cell = workbook.add_format({'font_color': 'white', 'bg_color': 'orange', 'bold': True})
    orange_time_cell = workbook.add_format({'font_color': 'white', 'bg_color': 'orange', 'bold': True, 'num_format': 'hh:mm:ss'})
    yellow_time_cell = workbook.add_format({'font_color': 'black', 'bg_color': 'yellow', 'bold': True, 'num_format': 'hh:mm:ss'})
    green_cell = workbook.add_format({'font_color': 'white', 'bg_color': 'green', 'bold': True})
    black_cell = workbook.add_format({'font_color': 'black'})
    time_cell = workbook.add_format({'num_format': 'hh:mm:ss'})
    white_cell = workbook.add_format({'font_color': 'white'})
    days_in_month = calendar.monthrange(year, month)[1]
    weekends = Create_Free_days()
    def Cell_Choose(i):
        if i == 0:
            return time_cell
        elif i == 1:
            return orange_time_cell
        elif i == 2:
            return red_time_cell
        elif i == 3:
            return yellow_time_cell
    
    workbook.add_worksheet("Spis treści")
    workbook.add_vba_project('vbaProject.bin')
    if month == 1:
        prev_month = 12
    else:
        prev_month = month - 1
    
    hyperlink_count = 1
    for key, value in pres_dict.items():
        fname = value[0]
        lname = value[1]
        smoker = smk_dict[value[2]]
        localization = city_dict[value[3]]
        department = dep_dict[value[4]]
        agreement = agr_dict[value[5]]
        company = company_dict[value[6]]
        position = pos_dict[value[7]]
        try:
            overtime_previous = value[9][0][1]
        except:
            overtime_previous = 666
        try:
            overtime_actual = value[10][0][1]
        except:
            overtime_actual = "Brak danych"
        
        worksheet = workbook.get_worksheet_by_name("Spis treści")
        worksheet.write_url('A' + str(hyperlink_count), "internal:'" + lname + " " + fname + "'!A1", string = lname + " " + fname)
        workbook.add_worksheet(lname + " " + fname)
        worksheet = workbook.get_worksheet_by_name(lname + " " + fname)
        worksheet.write_url('A1', "internal:'Spis treści'!A1", string = fname + " " + lname)
        
        worksheet.write(1, 0, agreement)
        worksheet.write(2, 0, company)
        worksheet.write(3, 0, position)
        worksheet.write(4, 0, "Nadgodziny %s:" % Month_to_String(prev_month))
        if overtime_previous != 666:
            worksheet.write(5, 0, overtime_previous)
        else:
            worksheet.write(5, 0, "Brak danych - ustawiam 0")
            overtime_previous = 0
        worksheet.write(6, 0, "Nadgodziny %s:" % Month_to_String(month))
        worksheet.write(7, 0, overtime_actual)
        worksheet.write(9, 0, "Dzień:")
        worksheet.write(9, 1, "Wejście:")
        worksheet.write(9, 2, "Wyjście:")
        worksheet.write(9, 3, "Komentarz:")
        worksheet.write(9, 4, "Razem:")
        worksheet.write(9, 5, "Razem (H):")
        worksheet.write(9, 6, "Etat:")
        if value[2] == 1: #PALACZ
            expected_total_time = 4
        else:
            expected_total_time = 0
        
        i = 1
        total_total_time = timedelta(hours=0)
        total_total_hours = 0
        entry_dict = {}
        exit_dict = {}
        
#____________________________________________RTL
        entries_list = []
        exits_list = []
        for entry in value[8]:
            if entry[1] == 1:
                entries_list.append(entry[2])
            if entry[1] == 2:
                exits_list.append(entry[2])
        
        dict_entry_exit = {}
        for exit_ in exits_list:
            for entry_ in entries_list:
                if entry_ < exit_:
                    dict_entry_exit[exit_] = entry_
                    #DEBUG dict_entry_exit[exit_.strftime("%Y-%m-%d %H:%M:%S")] = entry_.strftime("%Y-%m-%d %H:%M:%S")
#____________________________________________RTL
        for key in dict_entry_exit:
            entries_list.remove(dict_entry_exit[key])
            
        print(entries_list)

            
        #print(entries_list)
        
        while i <= days_in_month:
            expected_time = Expected_Time(key)
            actual_date = "%s-%s-%s" % (year, Number_to_String(month), Number_to_String(i))
            if Number_to_String(i-1) == 0:
                if Number_to_String(month-1) == 0:
                    previous_date = "%s-%s-%s" % (str(int(year)-1), Number_to_String(month), Number_to_String(i))
                else:
                    previous_date = "%s-%s-%s" % (year, Number_to_String(month-1), Number_to_String(i))
            else:
                previous_date = "%s-%s-%s" % (year, Number_to_String(month), Number_to_String(i-1))
                
            
            for item in value[8]:
                if item[2].strftime("%Y-%m-%d") == actual_date:
                    if item[3] != None:
                        worksheet.write(i+9, 3, item[3])
                    #RTL
                    if item[1] == 2:
                        try:
                            entry_dict[actual_date] = dict_entry_exit[item[2]]
                            exit_dict[actual_date] = item[2]
                            
                            total_time, total_hours = Generate_Overtime(key, agreement, entry_dict[actual_date], exit_dict[actual_date])
                            total_total_time += total_time
                            total_total_hours += total_hours
                            if len(str(total_time)) == 7:
                                total_time_for_cell_h = int(str(total_time)[:1])
                                total_time_for_cell_m = int(str(total_time)[2:4])
                            elif len(str(total_time)) == 8:
                                total_time_for_cell_h = int(str(total_time)[:2])
                                total_time_for_cell_m = int(str(total_time)[3:5])
                            if dict_entry_exit[item[2]].strftime("%Y-%m-%d") == actual_date:
                                row_number_ = i+9
                            else:
                                row_number_ = i+8
                            worksheet.write(row_number_, 1, entry_dict[actual_date].strftime("%H:%M:%S"), Cell_Choose(Cell_Type_Entry_Exit(key, int(entry_dict[actual_date].strftime("%H")), int(entry_dict[actual_date].strftime("%M")), "entry")))
                            worksheet.write(row_number_, 2, exit_dict[actual_date].strftime("%H:%M:%S"), Cell_Choose(Cell_Type_Entry_Exit(key, int(exit_dict[actual_date].strftime("%H")), int(exit_dict[actual_date].strftime("%M")), "exit")))
                            worksheet.write(row_number_, 4, str(total_time), Cell_Choose(Cell_Type_Entry_Exit(key, total_time_for_cell_h, total_time_for_cell_m, "total")))
                            worksheet.write(row_number_, 5, total_hours)
                            worksheet.write(row_number_, 6, expected_time)
                        except:
                            worksheet.write(i+9, 1, "ERROR FETCHING DATA")
                    #PDA
                    # if item[1] == 1:
                    #     entry_dict[actual_date] = item[2]
                    #     worksheet.write(i+9, 1, entry_dict[actual_date].strftime("%H:%M:%S"), Cell_Choose(Cell_Type_Entry_Exit(key, int(entry_dict[actual_date].strftime("%H")), int(entry_dict[actual_date].strftime("%M")), "entry")))
                    # elif item[1] == 2:
                    #     exit_dict[actual_date] = item[2]
                    #     worksheet.write(i+9, 2, exit_dict[actual_date].strftime("%H:%M:%S"), Cell_Choose(Cell_Type_Entry_Exit(key, int(exit_dict[actual_date].strftime("%H")), int(exit_dict[actual_date].strftime("%M")), "exit")))
                        
                    #     total_time, total_hours = Generate_Overtime(key, agreement, entry_dict[actual_date], exit_dict[actual_date])
                    #     total_total_time += total_time
                    #     total_total_hours += total_hours
                        
                    #     if len(str(total_time)) == 7:
                    #         total_time_for_cell_h = int(str(total_time)[:1])
                    #         total_time_for_cell_m = int(str(total_time)[2:4])
                    #     elif len(str(total_time)) == 8:
                    #         total_time_for_cell_h = int(str(total_time)[:2])
                    #         total_time_for_cell_m = int(str(total_time)[3:5])
                            
                    #     worksheet.write(i+9, 4, str(total_time), Cell_Choose(Cell_Type_Entry_Exit(key, total_time_for_cell_h, total_time_for_cell_m, "total")))
                    #     worksheet.write(i+9, 5, total_hours)
                    #     worksheet.write(i+9, 6, expected_time)

                    elif item[1] == 3 or item[1] == 4:
                        continue
                    elif item[1] in (5, 7, 8, 10, 12, 13, 14, 15, 17, 18, 19, 22, 23, 24, 25, 26):
                        worksheet.write(i+9, 2, action_dict[item[1]], green_cell)
                        worksheet.write(i+9, 4, "%s:00:00" % expected_time, time_cell)
                        worksheet.write(i+9, 5, expected_time)
                        worksheet.write(i+9, 6, expected_time)
                        total_total_hours += expected_time
                        #print("DODAJE %s nadgodzin poniewaz akcja to %s - data %s" % (total_total_hours, item[1], actual_date))
                        total_total_time += timedelta(hours=expected_time)
                    else:
                        if item[1] == 1:
                            if item[2] in entries_list:
                                worksheet.write(i+9, 1, item[2].strftime("%H:%M:%S"))
                                worksheet.write(i+9, 2, "Brak wyjścia")
                        else:
                            worksheet.write(i+9, 2, action_dict[item[1]], red_cell)
                            worksheet.write(i+9, 6, expected_time)
                    
                    
                        
                    
            if actual_date in weekends:
                worksheet.write(i+9, 0, actual_date, green_cell)
            else:
                worksheet.write(i+9, 0, actual_date)
                expected_total_time += 8
            i+=1
            
        worksheet.write(i+10, 4, "%s:%s" % (math.floor(total_total_time.total_seconds() / 3600), math.floor(total_total_time.total_seconds() % 3600 / 60)))
        worksheet.write(i+10, 5, total_total_hours)
        worksheet.write(i+10, 6, int(str(expected_total_time)))
        if value[2] == 1: #PALACZ
            worksheet.write(i+5, 7, "Palacz (+4)", red_cell)
        worksheet.write(1, 3, "+%s (%s)" % (Month_to_String(prev_month), overtime_previous))
        worksheet.write(1, 4, total_total_hours + overtime_previous)
        worksheet.write(2, 3, "Nadg:")
        worksheet.write(2, 4, total_total_hours - int(str(expected_total_time)))
        worksheet.write(3, 3, "Nadg razem:")
        worksheet.write(3, 4, overtime_previous + total_total_hours - expected_total_time)
        worksheet.write(4, 3, "Razem:")
        worksheet.write(4, 4, total_total_hours + overtime_previous + (total_total_hours - int(str(expected_total_time))))
        worksheet.insert_button(
       'F4',
            {
                'macro': "'update_db \"%s\", Evaluate(\"F%s\"), \"%s\"'" % (str(key), str(i+9), str(year) + "-" + str(Number_to_String(month))),
                'caption': 'Aktualizuj nadgodziny',
                'width': 200, 'height': 20
            }
        )
        #print("'update_db \"%s\", Evaluate(\"F%s\"), \"%s\"'" % (str(key), str(i+9), (str(year) + "-" + str(Number_to_String(month)))))
        worksheet.autofit()
        worksheet.set_column(0, 0, 10)
        hyperlink_count+=1

    workbook.close()
    
    if just_worker == 0 and just_department == 0:
        os.startfile(os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc.xlsm"))
    elif just_department != 0:
        os.startfile(os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc_dep_%s.xlsm" % just_department))
    else:
        os.startfile(os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc_%s.xlsm" % list(pres_dict.keys())[0]))

