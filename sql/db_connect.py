from fnct.getpath import Get_Local_Path
import re
import os

home_directory = os.path.expanduser('~')
home_directory = os.path.join(home_directory, "Documents", "PajerApp")
pajer_dbfile = os.path.join(home_directory, "params.txt")
favicon_imgfile = os.path.join(home_directory, "favicon.ico")

if os.path.exists(home_directory) == False:
    os.system('mkdir %s' % home_directory)

local_path_app = Get_Local_Path()
filepath = local_path_app + "\\sql\\params.txt"

if os.path.isfile(pajer_dbfile) == False:
    os.system('copy "%s" "%s"' % (filepath, home_directory))
if os.path.isfile(favicon_imgfile) == False:
    favicon_1 = local_path_app + "\\img\\favicon.ico"
    logo1 = local_path_app + "\\img\\logo.png"
    logo2 = local_path_app + "\\img\\logo2.png"
    os.system('copy "%s" "%s"' % (favicon_1, home_directory + "\\"))
    os.system('copy "%s" "%s"' % (logo1, home_directory + "\\"))
    os.system('copy "%s" "%s"' % (logo2, home_directory + "\\"))

try:
    db_file = open(pajer_dbfile, 'r')
    db_params = db_file.readlines()
    connection_dict = {}

    connection_dict['login'] = re.findall(r'"([^"]*)"', db_params[0])[0]
    connection_dict['password'] = re.findall(r'"([^"]*)"', db_params[1])[0]
    connection_dict['host'] = re.findall(r'"([^"]*)"', db_params[2])[0]
    connection_dict['db'] = re.findall(r'"([^"]*)"', db_params[3])[0]
    connection_dict['port'] = re.findall(r'"([^"]*)"', db_params[4])[0]
    db_file.close()

    dbLogin = connection_dict['login']
    dbPassword = connection_dict['password']
    dbHost = connection_dict['host']
    dbDatabase = connection_dict['db']
    dbPort = connection_dict['port']
except:
    db_file = open(pajer_dbfile, 'w')
    db_file.write('dbLogin="firstrun"\n')
    db_file.write('dbPassword=""\n')
    db_file.write('dbHost=""\n')
    db_file.write('dbDatabase=""\n')
    db_file.write('dbPort=""')
    db_file.close()
    
    dbLogin = ""
    dbPassword = ""
    dbHost = ""
    dbDatabase = ""
    dbPort = ""