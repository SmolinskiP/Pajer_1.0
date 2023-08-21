import mysql.connector as database
from wakeonlan import send_magic_packet
import paramiko

dbLogin = "rcp"
dbPassword = "PDArcpSERWIS"
dbHost = "p.pdaserwis.pl"
dbDatabase = "RFID"
dbPort = "3306"

def SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort):
    try:
        conn = database.connect(user = dbLogin, password = dbPassword, host = dbHost, database = dbDatabase, port = dbPort)
    except database.Error as e:
        print(f"Nie udalo sie polaczyc z baza danych MariaDB: {e}")
    return conn

malinowski = "0016377013"
skalski = "0016381385"
dabrowska = "0016321874"
szymon = "0016316108"
card_id = malinowski
conn = SQL_Connect(dbLogin, dbPassword, dbHost, dbDatabase, dbPort)

def WakeComputer(card_id):

    sql_query = "SELECT sprzet.mac, przypisanieip.ip FROM pracownicy LEFT JOIN przypisanieip ON przypisanieip.pracownik = pracownicy.id LEFT JOIN sprzet ON przypisanieip.komputer = sprzet.id WHERE pracownicy.karta = '" + card_id + "'"
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    mac_addr = get_sql.fetchall()[0][0]
    print(mac_addr)
    send_magic_packet(mac_addr, interface='10.0.10.156')
    
def WakeComputer2(card_id, conn):
    sql_query = "SELECT sprzet.mac, przypisanieip.ip FROM pracownicy LEFT JOIN przypisanieip ON przypisanieip.pracownik = pracownicy.id LEFT JOIN sprzet ON przypisanieip.komputer = sprzet.id WHERE pracownicy.karta = '" + card_id + "'"
    print(sql_query)
    get_sql = conn.cursor()
    get_sql.execute(sql_query)
    mac_addr = get_sql.fetchall()[0][0]
    print(mac_addr)
    try:
        cmd_to_execute = "sudo etherwake -i enp3s0f0 " + mac_addr
        print(cmd_to_execute)
    except Exception as e:
        print(e)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.10.1", username="wakeonlan", password="81d7a5c58", port=4224)
    try:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
    except Exception as e:
        print(e)
    ssh.close()
    
WakeComputer2(card_id, conn)
#or item in mac_addr:
#   print(item[0])

#mac_addr = mac_addr.replace(":", ".")
#print(mac_addr)

#
