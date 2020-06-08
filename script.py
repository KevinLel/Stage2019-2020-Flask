#coding:latin-1

import datetime
import sqlite3

def script():
    dateActuelle = datetime.datetime
    if dateActuelle.hour == 0 and dateActuelle.minute == 0 and dateActuelle.second == 0
        try:
            connection = sqlite3.connect('database.sqlite3')
        except Error as e:
            print(e)
        c = connection.cursor()
        c.execute("SELECT * FROM PAIEMENTS WHERE dateCreation = ?", dateActuelle.today())
        for element in c.fetchall():
            if element.date
                c.execute("INSERT INTO Bail VALUES ")
