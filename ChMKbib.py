#!/usr/bin/python

import os, sys, livestatus, time, calendar


def log_Since_Time(socket_path):
    import os, sys, livestatus, time, calendar
    t=calendar.timegm(time.gmtime())    
    zeitraum=input("Auf welchen Zeitraum sollen die Ergebnisse eingegrenzt werden? Eingabe in Minuten:")
    zeitraum=zeitraum*60
    t=t-zeitraum
    try:
        services = livestatus.SingleSiteConnection(socket_path).query_table("GET log\nFilter: time >= %d\nFilter: class = 1\nColumns: host_name service_description time state\nOutputFormat: python"%t)
        for host_name, service_description,time, state in services:
            print "%-12s %-25s %-12s %-5s" % (host_name, service_description,time, state)

    except Exception, e:
        print "Livestatus Error %s" % str(e)

##########################################################################################
def local_Connection():
    try:
        omd_root = os.getenv("OMD_ROOT")
        socket_path = "unix:" + omd_root + "/tmp/run/live"
        return socket_path

    except:
        sys.stderr.write("Fehler! OMD!")
        sys.exit(1)

##########################################################################################
def show_Hosts(socket_path):
    try:
        print "\nHosts:"
        hosts = livestatus.SingleSiteConnection(socket_path).query_table("GET hosts\nColumns: name alias address")
        for name, alias, address in hosts:
            print "%-16s %-16s %s" % (name, address, alias)
    except Exception, e:
        print "Livestatus error %s" % str(e)


##########################################################################################
def show_Services(socket_path):
    try:
        print "\nServices mit genauer Beschreibung"
        t = time.ctime()
        print "Zeitpunkt der Abfrage: %s\n" % t
        services=livestatus.SingleSiteConnection(socket_path).query_table("GET services\nColumns: host_name description state")

        for host_name, description, state in services:
            print "%-10s %-20s %s" % (host_name, description, state)
        fobj_out = open("/home/service/Schreibtisch/Testprogramme/ServiceLOG.txt","a")
        fobj_out.write("Zeitpunkt der Abfrage: %s\n" %t)
        for host_name in services:
            fobj_out.write("%s\n" %(host_name))

    except Exception, e:
        print "Livestatus Error %s" % str(e)
    return services

#########################################################################################
def show_New_Logs(socket_path):
    logs = []
    try:
       t = calendar.timegm(time.gmtime())
       logs = livestatus.SingleSiteConnection(socket_path).query_table("GET log\nColumns: host_name service_description time state\nWaitTrigger: log\nFilter: time >= %d\nFilter: class = 1\nOutputFormat: python"%t)
       if logs:
           print logs, t
      
    except Exception, e:
        print "Livestatus Error %s" % str(e)

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





    try:
       services=livestatus.SingleSiteConnection(socket_path).query_table("GET services\nColumns: host_name description state")
       t = calendar.timegm(time.gmtime())
       for host_name, description, state in services:
           
           logs = livestatus.SingleSiteConnection(socket_path).query_table("GET log\nWaitTrigger: downtime\nWaitTimeout: 5000\nFilter: time >= %d\nColumns: host_name service_description time state" %(t))
       if logs:
           print logs, t
           return logs
    except Exception, e:
        print "Livestatus Error %s" % str(e)

#    return logs

###############################################################################

def show_Availability(socket_path):

    try:
        t=calendar.timegm(time.gmtime())
        z=input("Geben Sie den Zeitraum ein, in dem die Verfuegbarkeit der Services bestimmt werden soll. (Eingabe in Stunden):")
        k=z*3600
        k=t-k
       
        availability=livestatus.SingleSiteConnection(socket_path).query_table("GET statehist\nColumns: host_name service_description\nFilter: time < %d\nFilter: time >= %d\nStats: sum duration_part_ok\nStats: sum duration_part_warning\nStats: sum duration_part_critical\nStats: sum duration_part_unknown\nStats: sum duration_part_unmonitored" %(t,k))
 
       
       
        for line in availability:
            print line
    except Exception, e:
        print "Livestatus Error %s" % str(e)