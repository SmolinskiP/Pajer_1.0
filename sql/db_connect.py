from fnct.getpath import Get_Local_Path
import re

filepath = Get_Local_Path() + "\\sql\\params.txt"
db_file = open(filepath, 'r')
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