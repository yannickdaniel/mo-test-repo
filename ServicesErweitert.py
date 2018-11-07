#Dieses Programm zeigt die Services zusammen mit Hostname, Beschreibung des Services und dem Zustand an.
#Ausserdem wird alles in einer Textdatei abgespeichert -> Damit kann vielleicht spaeter die OIS Schnittstelle befuellt werden??
#Die Daten werden mit einer Zykluszeit von 60s abgefragt.
#!/usr/bin/python

import os, sys
import livestatus
import time

while(1):

    try: 
        omd_root = os.getenv("OMD_ROOT")
        socket_path = "unix:" + omd_root + "/tmp/run/live"

    except:
        sys.stderr.write("This test is intendet to run in OMD")
        sys.exit(1)

    try:
        print "\nServices mit genauerer Beschreibung"
        t=time.ctime()
        print "Zeitpunkt der Abfrage: %s\n" % t 
        services = livestatus.SingleSiteConnection(socket_path).query_table("GET services\nColumns: host_name description state")

        for host_name, description, state in services:
            print "%-10s %-20s %s" % (host_name, description, state)
        fobj_out = open("/home/service/Schreibtisch/Testprogramme/ServiceLOG.txt","a")
        fobj_out.write("Zeitpunkt der Abfrage: %s\n" %t) 
        for host_name in services:
            fobj_out.write("%s\n" % (host_name))


    except Exception, e:
         print "Livestatus error %s" %str(e)
    time.sleep(60)                   

