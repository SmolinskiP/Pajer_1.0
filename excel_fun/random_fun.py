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
    print("EMP -%s, Wejscie - %s Wyjscie -%s" % (emp_id, h_entry, h_exit))
    total_time = h_exit - h_entry
    hours = math.floor(total_time.total_seconds() / 3600)
    minutes = math.floor(total_time.total_seconds() % 3600 / 60)
    if minutes >= 55:
        hours+=1
    elif minutes >= 30:
        hours+=0.5
        
    return total_time, hours

def Cell_Type_Entry_Exit(emp_id, time, time_m, entry_type):
    if emp_id in (8, 7, 683, 14, 187, 21, 710, 23): #BARBARA BALUTA, ANNA STANOWSKA, #ZANETA PAWLAK, #ELZBIETA DABROWSKA, #PAULINA DABROWSKA, KASIA SZYDLOWSKA, ROBERT SKIBINSKI, KRYSTIAN BURACZYNSKI
        if entry_type == "entry" and time >= 8 and time_m > 0:
            return 1
        elif entry_type == "exit" and time < 15:
            return 1
        elif entry_type == "total" and time < 7 and emp_id in (8, 710): #BARBARA BALUTA, ROBERT SKIBINSKI
            return 2
        elif entry_type == "total" and time < 8 and emp_id in (7, 683, 14, 187, 21, 23): #ANNA STANOWSKA, #ZANETA PAWLAK, #ELZBIETA DABROWSKA, #PAULINA DABROWSKA, KASIA SZYDLOWSKA, KRYSTIAN BURACZYNSKI
            return 2
        elif entry_type == "total" and ((time == 7  and time_m >= 30) or time > 7) and emp_id in (8, 710):
            return 3
        elif entry_type == "total" and ((time == 8  and time_m >= 30) or time > 8) and emp_id in (7, 683, 14, 187, 21, 23):
            return 3
        else:
            return 0
    elif emp_id == 679: #BARBARA BALUTA ZLECENIE
        if entry_type == "entry" and time != 15:
            return 1
        elif entry_type == "exit" and time < 16:
            return 1
        elif entry_type == "total" and time < 1:
            return 2
        elif entry_type == "total" and ((time == 1 and time_m >= 30) or time > 1):
            return 3
        else:
            return 0
    elif emp_id == 122: #ROBERT KOWALSKI
        if entry_type == "entry" and time >= 8 and time_m > 0:
            return 1
        elif entry_type == "exit" and time < 16 and time_m < 45:
            return 1
        elif entry_type == "total" and time < 8:
            return 2
        elif entry_type == "total" and ((time == 8  and time_m >= 30) or time > 8):
            return 3
        else:
            return 0
    else:
        if entry_type == "entry" and time >= 8 and time_m > 0:
            return 1
        elif entry_type == "exit" and time < 16:
            return 1
        elif entry_type == "total" and time < 8:
            return 2
        elif entry_type == "total" and ((time == 8  and time_m >= 30) or time > 8):
            return 3
        else:
            return 0
    
    

def Expected_Time(emp_id):
    if emp_id in (8, 710): #BASKA ROBERT
        expected_time_day = 7
    elif emp_id == 679: #BASKA ZLECENIE
        expected_time_day = 1
    else:
        expected_time_day = 8
    return expected_time_day