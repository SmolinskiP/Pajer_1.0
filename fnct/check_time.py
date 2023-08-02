def Check_Time(time_from, time_to):
    print(time_from)
    if int(time_from[0])*60 + int(time_from[1]) >= int(time_to[0])*60 + int(time_to[1]):
        print(int(time_from[0])*60 + int(time_from[1]))
        print("WIEKSZE NIZ")
        print(int(time_to[0])*60 + int(time_to[1]))
        return False
    else:
        return True