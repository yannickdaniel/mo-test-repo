#Dieses Programm soll einmal die gesamten Services mit ihrem Status auflisten, abspeichern und danach nurnoch geaenderte Services mit einem Zeitstempel.
#!/usr/bin/python

import os, sys
import livestatus
import time

Erstanlauf=False
gleicheWerte=0
once=False
while(1):
    if once==False:
        try: 
            omd_root = os.getenv("OMD_ROOT")
            socket_path = "unix:" + omd_root + "/tmp/run/live"

        except:
            sys.stderr.write("Fehler! OMD!")
            sys.exit(1)

    try:
        t=time.ctime()
        services = livestatus.SingleSiteConnection(socket_path).query_table("GET services\nColumns: host_name description state\nKeepAlive: on")
    
        if Erstanlauf==False:
             print "\nServices mit genauerer Beschreibung:"
             print "Zeitpunkt der Abfrage: %s\n" % t 
                
             for host_name, description, state in services:
                print "%-10s %-20s %s" % (host_name, description, state)
                fobj_out = open("/home/service/Schreibtisch/Testprogramme/ServiceLOG.txt","a")
                fobj_out.write("Zeitpunkt der Abfrage: %s\n" %t) 
             for host_name in services:
                fobj_out.write("%s\n" % (host_name))
             Erstanlauf = True

        else:     
             for state in services:
                 for alterState in alteWerte:
                     if state[1] == alterState[1]:
                         if state[0] == alterState[0]:
                             if state[2] != alterState[2]:
                                 print("\nNeuer Status: %s" % t)
                                 print("%s\n" % state)
                        
    except Exception, e:
         print "Livestatus error %s" %str(e)

    alteWerte=services
   
    time.sleep(35)                   

