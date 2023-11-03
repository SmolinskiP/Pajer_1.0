import math

def Number_to_String(number):
    if number < 10:
        number = "0" + str(number)
    else:
        number = str(number)
    return number

def Month_to_String(month):
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
    

def Generate_Overtime(emp_id, emp_agreement, h_entry, h_exit):
        
    total_time = h_exit - h_entry
    hours = math.floor(total_time.total_seconds() / 3600)
    minutes = math.floor(total_time.total_seconds() % 3600 / 60)
    if minutes > 55:
        hours+=1
        
    return total_time, hours

def Expected_Time(emp_id):
    if emp_id == 0:
        expected_time_day = 7
    else:
        expected_time_day = 8
    return expected_time_day