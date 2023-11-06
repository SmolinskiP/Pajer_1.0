import sys
from time import sleep
import mysql.connector as database

emp_id = sys.argv[1]
overtime = sys.argv[2]
month = sys.argv[3]

print("Wykonuje skrypt z parametrami:\n")
print("ID pracownika: %s" % emp_id)
print("Ilosc nadgodzin: %s" % overtime)
print("Data: %s\n" % month)

def SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort):
    try:
        conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase, port = dbPort)
        print("Połączono z bazą danych '%s' jako użytkownik '%s'" % (dbDatabase, dbLogin))
        return conn
    except database.Error as e:
        print(f"Nie udało się połączyć z bazą danych MariaDB: {e}")
        messagebox.showerror(title="Błąd połączenia z bazą danych", message=f"Brak dostępu do bazy danych\nNajprawdopodobniej nieprawidłowe parametry połączenia\nTreść błędu:\nNie udało się połączyć z bazą danych MariaDB: {e}")
   
print("Łączenie z bazą danych...")
conn = SQL_Connect("rcp", "PDArcpSERWIS", "10.0.10.1", "RFID", "3306")
cursor = conn.cursor()

print("Weryfikuję czy pracownik ma już wpis w bazie...")
sql_query = "SELECT nadgodziny FROM nadgodziny WHERE pracownik = " + str(emp_id) + " AND data LIKE '" + month + "%'"
cursor.execute(sql_query)
result = cursor.fetchall()

if result == []:
    print("Nie znaleziono wpisu, dodaję nowy...")
    sql_query = "INSERT INTO nadgodziny (pracownik, data, nadgodziny) VALUES (%s, '%s', %s)" % (str(emp_id), str(month) + "-15", str(overtime))
else:
    print("Znaleziono już wpis dla tego pracownika, uaktualniam...")
    sql_query = "UPDATE nadgodziny SET nadgodziny = %s WHERE pracownik = %s AND data LIKE '%s'" % (str(overtime), str(emp_id), str(month) + "%")
    
print(sql_query)
cursor.execute(sql_query)
conn.commit()
conn.close()
print("\nDodawanie pomyślne, można zamknąć to okno. I tak się zamknie za 10 sekund jak coś ;)")
sleep(10)