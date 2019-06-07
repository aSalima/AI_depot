import mysql.connector
import pyodbc
import csv
import constantes as cs
from mysql.connector import Error

# ********************************************************** #
# ********************** Connexion mySql ******************* #
# ********************************************************** #
'''
connMySql = mysql.connector.connect(host=cs.serverMySql, database=cs.databaseMySql, user=cs.usernameMySql, password=cs.passwordMySql)
if connMySql.is_connected():
        cursor = connMySql.cursor()
        #cursor.execute("SELECT id, summary FROM mantis_local.mantis_bug_table limit 60")
        cursor.execute("SELECT B.id as id_mantis, BT.description FROM mantis_local.mantis_bug_table B, mantis_local.mantis_bug_text_table BT where BT.id = B.bug_text_id;")
        lines = cursor.fetchall()
        with open('mantis.csv', 'w', encoding='UTF-8') as newMantisFile:
            csvWriterMantis = csv.writer(newMantisFile, delimiter=',')
            for line in lines:
                csvWriterMantis.writerow(line)

# ********************************************************** #
# ****************** Connexion Sql Server ****************** #
# ********************************************************** #

connSqlServer = pyodbc.connect('DRIVER={SQL Server};SERVER='+cs.serverSqlServer+';DATABASE='+cs.databaseSqlServer+';UID='+cs.usernameSqlServer+';PWD='+ cs.passwordSqlServer)
cursorSqlServer = connSqlServer.cursor()
cursorSqlServer.execute("SELECT TOP(100) DA.[Numéro DA Cristal],DA.[Objet],ActDA.[Commentaire],ActDA.[EchangeClient] FROM [cristalTestDB].[dbo].[BL_v_Liste_DA] DA, [cristalTestDB].[dbo].[BL_Liste_ActivitesDA] ActDA WHERE ActDA.[Numéro DA Cristal]=DA.[Numéro DA Cristal];")
print("connexion sql server reussie")
rows = cursorSqlServer.fetchall()
with open('cristal.csv', 'w', encoding='UTF-8') as cristalFile:
    csvWriterCristal = csv.writer(cristalFile, delimiter=',')
    for row in rows:
        csvWriterCristal.writerow(row)
'''

def no_accent(text):
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â']
    zero_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a']
    for i in range(len(accent)):
        text = text.replace(accent[i], zero_accent[i])
    return text

# ********************************************************** #
# ********************** Connexion mySql ******************* #
# ********************************************************** #

def connMySql(host, database, user, password, query):
    connMySql = mysql.connector.connect(host=host, database=database, user=user, password=password)
    if connMySql.is_connected():
        cursor = connMySql.cursor()
        cursor.execute(query)
        lines = cursor.fetchall()
        return lines

# ********************************************************** #
# ****************** Connexion Sql Server ****************** #
# ********************************************************** #

def connSqlServer(host, database, user, password, query):
    connSqlServer = pyodbc.connect('DRIVER={SQL Server};SERVER=' + host + ';DATABASE=' + database + ';UID=' + user + ';PWD=' + password)
    cursorSqlServer = connSqlServer.cursor()
    cursorSqlServer.execute(query)
    print("connexion sql server reussie")
    lines = cursorSqlServer.fetchall()
    return lines

# ********************************************************** #
# *********************** BD To CSV  *********************** #
# ********************************************************** #

def sqlServerToCsv(lines, file):
    with open(file, 'w', encoding='UTF-8') as newFile:
        csvWriter = csv.writer(newFile, delimiter=',')
        for line in lines:
            csvWriter.writerow(line)
    return file

def mySqlToCsv(lines, file):
    with open(file, 'w') as newFile:
        csvWriter = csv.writer(newFile, delimiter=',')
        for line in lines:
            newLine=[]
            newLine.append(line[0])
            line1 = no_accent(str(line[1]))
            newLine.append(line1)
            csvWriter.writerow(newLine)
    return file

#mySqlToCsv(connMySql(cs.serverMySql, cs.databaseMySql, cs.usernameMySql, cs.passwordMySql, "SELECT id, summary FROM mantis_local.mantis_bug_table limit 60;"),'MM.csv')

#bdToCsv(connSqlServer(cs.serverSqlServer, cs.databaseSqlServer, cs.usernameSqlServer, cs.passwordSqlServer,"SELECT TOP(100) DA.[Numéro DA Cristal],DA.[Objet],ActDA.[Commentaire],ActDA.[EchangeClient] FROM [cristalTestDB].[dbo].[BL_v_Liste_DA] DA, [cristalTestDB].[dbo].[BL_Liste_ActivitesDA] ActDA WHERE ActDA.[Numéro DA Cristal]=DA.[Numéro DA Cristal];"),'CC.csv')



query = 'SELECT id, summary FROM mantis_local.mantis_bug_table;'
lines = connMySql(cs.serverMySql, cs.databaseMySql, cs.usernameMySql, cs.passwordMySql, query)