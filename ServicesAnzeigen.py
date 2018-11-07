import os, sys
import livestatus

try:
        omd_root = os.getenv("OMD_ROOT")
        socket_path = "unix:" + omd_root + "/tmp/run/live"

except:
        sys.stderr.write("This example is intended to run in an OMD site")
        sys.exit(1)
                
#Mehrere Connections:
conn = livestatus.SingleSiteConnection(socket_path)
num_up = conn.query_value("GET hosts\nStats: hard_state = 0")

stats = conn.query_row(
      "GET services\n"

      "Stats: state = 0\n"
      "Stats: state = 1\n"
      "Stats: state = 2\n"
      "Stats: state = 3\n")
print "Service stats: %d/%d/%d/%d" %tuple(stats)
#print "%s " % num_up


    


