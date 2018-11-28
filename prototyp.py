#!/usr/bin/python
# -*- encoding: iso-8859-15 -*-


import os, sys, livestatus, time, calendar
import ChMKbib

abbruch = 0

def menue(menuePunkt):
    if menuePunkt == 1:
        ChMKbib.show_Hosts(socket_path)
    elif menuePunkt == 2:
        ChMKbib.show_Services(socket_path)
    elif menuePunkt == 3:
        ChMKbib.log_Since_Time(socket_path)
    elif menuePunkt == 4:
        ChMKbib.show_Availability(socket_path)
    elif menuePunkt == 5:
        dataTextfile=ChMKbib.show_New_Logs(socket_path)
        ChMKbib.write_To_Textfile(dataTextfile)
    elif menuePunkt == 6:
        ChMKbib.send_Command(socket_path)
    return None

socket_path=ChMKbib.start_Connection()

while(abbruch == 0):
    print("\n\n#################################################\n")
    print("Bitte einen der folgenden Menü-Punkte auswählen:")
    print("1. Hosts anzeigen")
    print("2. Services anzeigen")
    print("3. Log anzeigen")
    print("4. Verfügbarkeit anzeigen")
    print("5. Events anzeigen")
    print("6. Command schicken")
    menuePunkt = input("Menü-Punkt auswählen: ")
    print("\n#################################################\n\n")
    menue(menuePunkt)
    #abbruch = raw_input("Zum Abbrechen eine Taste betaetigen.")

    



