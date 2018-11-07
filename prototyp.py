#!/usr/bin/python

import os, sys, livestatus, time, calendar
import ChMKbib



socket_path=ChMKbib.local_Connection()

ChMKbib.show_Hosts(socket_path)

ChMKbib.log_Since_Time(socket_path)

ChMKbib.show_Services(socket_path)

ChMKbib.show_Availability(socket_path)

while(1):    
    dataTextfile=ChMKbib.show_New_Logs(socket_path)
    ChMKbib.write_To_Textfile(dataTextfile)


#    ChMKbib.show_Logs_Test(socket_path)
    time.sleep(1)
#    print ("Test") 
