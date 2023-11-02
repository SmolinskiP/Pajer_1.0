def Number_to_String(number):
    if number < 10:
        number = "0" + str(number)
    else:
        number = str(number)
    return number
