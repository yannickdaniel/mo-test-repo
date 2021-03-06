#!/usr/bin/python2.7
# -*- encoding: iso-8859-15 -*-

import os, sys, livestatus, time, calendar


def log_Since_Time(socket_path):
    import   livestatus, time, calendar
    t=calendar.timegm(time.gmtime())    
    zeitraum=input("Auf welchen Zeitraum sollen die Ergebnisse eingegrenzt werden? Eingabe in Minuten:")
    zeitraum=zeitraum*60
    t=t-zeitraum
    try:
        services = livestatus.SingleSiteConnection(socket_path).query_table("GET log\nFilter: time >= %d\nFilter: class = 1\nColumns: host_name service_description time state\nOutputFormat: python"%t)
        for host_name, service_description,time, state in services:
            print ("%-12s %-25s %-12s %-5s" % (host_name, service_description,time, state))

    except Exception as e:
        print ("Livestatus Error %s" % str(e))

##########################################################################################
def start_Connection():
    try:
        conn = raw_input("Lokale oder TCP Verbindung?(local / tcp)\nEingabe:")
        inp = ["local", "lokal", "Lokal"]
        if conn in inp:
            omd_root = os.getenv("OMD_ROOT")
            socket_path = "unix:" + omd_root + "/tmp/run/live"
        else:
            socket_path = "tcp:localhost:6557"
        return socket_path

    except:
        sys.stderr.write("Fehler! OMD!")
        sys.exit(1)

##########################################################################################
def show_Hosts(socket_path):
    try:
        print ("\nHosts:")
        hosts = livestatus.SingleSiteConnection(socket_path).query_table("GET hosts\nColumns: name alias address state")
        for name, alias, address, state in hosts:
            print ("%-16s %-16s %-15s %15s" % (name, address, alias, state))
    except Exception as e:
        print ("Livestatus error %s" % str(e))


##########################################################################################
def show_Services(socket_path):
    try:
        print ("\nServices mit genauer Beschreibung")
        t = time.ctime()
        print ("Zeitpunkt der Abfrage: %s\n" % t)
        services=livestatus.SingleSiteConnection(socket_path).query_table("GET services\nColumns: host_name description state")

        for host_name, description, state in services:
            print ("%-10s %-20s %s" % (host_name, description, state))
        fobj_out = open("/home/service/Schreibtisch/Testprogramme/ServiceLOG.txt","a")
        fobj_out.write("Zeitpunkt der Abfrage: %s\n" %t)
        for host_name in services:
            fobj_out.write("%s\n" %(host_name))

    except Exception as e:
        print ("Livestatus Error %s" % str(e))
    return services

#########################################################################################
def show_New_Logs(socket_path):
    logs = []
    try:
       t = calendar.timegm(time.gmtime())
       logs = livestatus.SingleSiteConnection(socket_path).query_table("GET log\nColumns: host_name service_description time state\nWaitTrigger: log\nFilter: time >= %d\nFilter: class = 1\nOutputFormat: python"%t)
       if logs:
           print (logs, t)
      
    except Exception as e:
        print ("Livestatus Error %s" % str(e))

    return logs

#########################################################################################
def write_To_Textfile(data):
    fobj_out = open("Textfile.txt","a")
    t = time.ctime()
    for line in data:
        fobj_out.write("%s\n" %t)
        fobj_out.write("%s\n" %line)

#########################################################################################
def show_Logs_Test(socket_path):
    pass
   # try:
    #   services=livestatus.SingleSiteConnection(socket_path).query_table("GET services\nColumns: host_name description state")
     #  t = calendar.timegm(time.gmtime())
      # for host_name, description, state in services:
       #    
        #   logs = livestatus.SingleSiteConnection(socket_path).query_table("GET log\nWaitTrigger: downtime\nWaitTimeout: 5000\nFilter: time >= %d\nColumns: host_name service_description time state" %(t))
       #if logs:
        #   print (logs, t)
         #  return logs
    #except Exception as e:
     #   print ("Livestatus Error %s" % str(e))

#    return logs

###############################################################################

def show_Availability(socket_path):

    try:
        t=calendar.timegm(time.gmtime())
        z=input("Geben Sie den Zeitraum ein, in dem die Verfügbarkeit der Services bestimmt werden soll. (Eingabe in Stunden):")
        k=z*3600
        k=t-k
       
        availability=livestatus.SingleSiteConnection(socket_path).query_table("GET statehist\nColumns: host_name service_description\nFilter: time < %d\nFilter: time >= %d\nStats: sum duration_part_ok\nStats: sum duration_part_warning\nStats: sum duration_part_critical\nStats: sum duration_part_unknown\nStats: sum duration_part_unmonitored" %(t,k))

        for line in availability:
            print(line)
    except Exception as e:
        print ("Livestatus Error %s" % str(e))

###############################################################################

def send_Command(socket_path):
   
    liste_anzeigen = raw_input("Wollen Sie eine Liste mit den verfügbaren Befehlen angezeigt bekommen?(Ja/Nein)\nEingabe: ")
    proceed =['y', 'Y', 'Ja', 'ja'] 
    read_obj = open("all_Commands.txt")
    all_Commands = read_obj.read()

    if liste_anzeigen in proceed: 
       print(all_Commands)  
 
    command = raw_input("Geben Sie den gewünschten Befehl ein: ")
    if command not in all_Commands:
        print("Fehler! Command nicht vorhanden!")
    else:
        #Hier den Command ausfueheren 
        hostname = raw_input("An welchem Host soll der Command ausgeführt werden? \n(Falls nicht, einfach mit ENTER bestätigen) \nEingabe: ")
        zusatz = raw_input("Werden zusätzliche Parameter fuer den Command benötigt? \n(Falls ja, bitte durch Strichpunkt trennen, nein mit ENTER bestätigen)\nEingabe: ")
        try: 
            #livestatus.SingleSiteConnection(socket_path).do_command("COMMAND %d %s;%s;" % (t,command,hostname))
            cmdStr = 'lq "COMMAND [$(date +%s)] ' + command + ';' + hostname + ';' + zusatz + '"'
            os.system(cmdStr)
                    
        except Exception as e:
            print("Livestatus Error: %s " % str(e))
    

