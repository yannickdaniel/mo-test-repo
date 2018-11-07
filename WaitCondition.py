#!/usr/bin/python
#Das Programm kann die Log Eintraege nach einer vorgegebenen Zeit heraus filtern
import os, sys
import livestatus
import time, calendar

try:
    omd_root = os.getenv("OMD_ROOT")
    socket_path = "unix:" + omd_root + "/tmp/run/live"

except:
    sys.stderr.write("Fehler! OMD!")
    sys.exit(1)

try:
  
    t=calendar.timegm(time.gmtime())
    zeitraum=input("Auf welchen Zeitraum sollen die Ergebnisse eingegrenzt werden? Eingabe in Minuten:")
    zeitraum=zeitraum*60
    t=t-zeitraum
    services = livestatus.SingleSiteConnection(socket_path).query_table("GET log\nFilter: time >= %d\nFilter: class = 1\nColumns: host_name service_description time state\nOutputFormat: python"%t)



    for host_name, service_description,time, state in services:
        print "%-12s %-25s %-12s %-5s" % (host_name, service_description,time, state)
   
   
   
   
   
   
  #  for line in services: 
   #     print line
   
     
except Exception, e:
    print "Livestatus error %s" % str(e)

