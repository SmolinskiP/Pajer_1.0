import mysql.connector as database
import xlsxwriter, calendar
from excel_fun.free_days import Create_Free_days
from excel_fun.random_fun import Number_to_String
from time import strftime
import os
import subprocess


def Create_Presence_Dict(conn, year, month, localization=0, department=0, employee=0):
    print("Generuję plik Excel do: %s" % os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc.xlsx"))
    print("Parametry pliku:\nRok: %s\nMiesiąc: %s\nLokalizacja: %s\nDział: %s\nPracownik: %s\n" % (year, month, localization, department, employee))
    get_sql = conn.cursor()
    employee_dict = {}
    
    if localization != 0:
        sql_query = "SELECT id, imie, nazwisko, palacz, dzial, umowa, firma, stanowisko FROM pracownicy WHERE active = 1 AND lokalizacja = %s ORDER BY nazwisko" % localization
        get_sql.execute(sql_query)
        sql_result = get_sql.fetchall()
        for item in sql_result:
            employee_dict[item[0]] = [item[1], item[2], item[3], localization, item[4], item[5], item[6], item[7], []]
    elif department != 0:
        sql_query = "SELECT id, imie, nazwisko, palacz, lokalizacja, umowa, firma, stanowisko FROM pracownicy WHERE active = 1 AND dzial = %s ORDER BY nazwisko" % department
        get_sql.execute(sql_query)
        sql_result = get_sql.fetchall()
        for item in sql_result:
            employee_dict[item[0]] = [item[1], item[2], item[3], item[4], department, item[5], item[6], item[7], []]
    elif employee != 0:
        sql_query = "SELECT id, imie, nazwisko, palacz, lokalizacja, dzial, umowa, firma, stanowisko FROM pracownicy WHERE active = 1 AND id = %s" % employee
        get_sql.execute(sql_query)
        sql_result = get_sql.fetchall()
        for item in sql_result:
            employee_dict[item[0]] = [item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], []]
        
    sql_query = "SELECT pracownik, action, time , komentarz FROM obecnosc WHERE pracownik IN ("
    for key, item in employee_dict.items():
        sql_query += "%s, " % key
    sql_query = sql_query[:-2]
    sql_query += ") AND TIME LIKE '%s%%' ORDER BY pracownik, time" % (str(year) + "-" + str(month))

    
    get_sql.execute(sql_query)
    sql_result = get_sql.fetchall()
    

    for item in sql_result:
        for key, value in employee_dict.items():
            if item[0] == key:
                employee_dict[key][8].append(item)
        
    return employee_dict

def Create_Presence_Excel(pres_dict, year, month, smk_dict, action_dict, dep_dict, company_dict, city_dict, agr_dict, pos_dict):
    #print(pres_dict)
    workbook = xlsxwriter.Workbook(os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc.xlsx"))
    red_cell = workbook.add_format({'font_color': 'white', 'bg_color': 'red', 'bold': True})
    orange_cell = workbook.add_format({'font_color': 'white', 'bg_color': 'orange', 'bold': True})
    green_cell = workbook.add_format({'font_color': 'white', 'bg_color': 'green', 'bold': True})
    black_cell = workbook.add_format({'font_color': 'black'})
    time_cell = workbook.add_format({'num_format': 'hh:mm:ss'})
    white_cell = workbook.add_format({'font_color': 'white'})
    days_in_month = calendar.monthrange(year, month)[1]
    weekends = Create_Free_days()
    
    workbook.add_worksheet("Spis treści")
    
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
        
        worksheet = workbook.get_worksheet_by_name("Spis treści")
        worksheet.write_url('A' + str(hyperlink_count), "internal:'" + lname + " " + fname + "'!A1", string = lname + " " + fname)
        workbook.add_worksheet(lname + " " + fname)
        worksheet = workbook.get_worksheet_by_name(lname + " " + fname)
        
        worksheet.write(0, 0, fname)
        worksheet.write(0, 1, lname)
        worksheet.write(1, 0, agreement)
        worksheet.write(1, 2, company)
        worksheet.write(0, 2, position)
        if value[2] == 1: #PALACZ
            worksheet.write(0, 6, "Palacz", red_cell)
            
        worksheet.write(3, 0, "Dzień:")
        worksheet.write(3, 1, "Wejście:")
        worksheet.write(3, 2, "Wyjście:")
        worksheet.write(3, 3, "Komentarz:")
        worksheet.write(3, 4, "Godzin razem:")

    
        
            
        i = 1
        entry_dict = {}
        exit_dict = {}
        while i <= days_in_month:
            actual_date = "%s-%s-%s" % (year, month, Number_to_String(i))
            for item in value[8]:
                if item[2].strftime("%Y-%m-%d") == actual_date:
                    if item[3] != None:
                        worksheet.write(i+3, 3, item[3])
                    if item[1] == 1:
                        worksheet.write(i+3, 1, item[2].strftime("%H:%M:%S"), time_cell)
                        entry_dict[actual_date] = item[2]
                    elif item[1] == 2:
                        worksheet.write(i+3, 2, item[2].strftime("%H:%M:%S"), time_cell)
                        exit_dict[actual_date] = item[2]
                        total_time = exit_dict[actual_date] - entry_dict[actual_date]
                        worksheet.write(i+3, 4, str(total_time), time_cell)
                    elif item[1] == 3 or item[1] == 4:
                        continue
                    else:
                        worksheet.write(i+3, 2, action_dict[item[1]])
                        worksheet.write(i+3, 4, "8:00:00", time_cell)
                    
                    
                        
                    
            if actual_date in weekends:
                worksheet.write(i+3, 0, actual_date, green_cell)
            else:
                worksheet.write(i+3, 0, actual_date)
            i+=1
            
    
        worksheet.autofit()
        hyperlink_count+=1

    workbook.close()
    os.startfile(os.path.join(os.path.expanduser('~'), "Documents", "Obecnosc.xlsx"))

