

import os, sys
import livestatus

try:
    omd_root = os.getenv("OMD_ROOT")
    socket_path = "unix:" + omd_root + "/tmp/run/live"
except:
    sys.stderr.write("This test is intended to run in OMD")
    sys.exit(1)

try:
    print "\nHosts:"
    hosts = livestatus.SingleSiteConnection(socket_path).query_table("GET hosts\nColumns: name alias address")
    for name, alias, address in hosts:
        print "%-16s %-16s %s" % (name, address, alias)
except Exception, e: 
    print "Livestatus error %s" % str(e)

