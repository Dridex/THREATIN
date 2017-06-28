#!/bin/bash
### BEGIN INIT INFO
# Provides: threatin
# Required-Start: $local_fs
# Required-Stop: $local_fs
# Short-Description: Start and Stop threat-agent service
# Description: threatin is a threat intellience platform framework
# Default-Start: start
# Default-Stop: stop
### END INIT INFO

PATH=/bin:/usr/bin:/sbin:/usr/sbin

DESC="threatin startup script"
NAME=threatin
DAEMON=threatind

do_start()
{

   service mysql start
   su -s /bin/bash -c '/opt/scripts/THREATIN/threat-agent/threatin-agent.py >/dev/null 2>/dev/null &' threatin
   sleep 2
   startpid=`pgrep -f threatin-agent.py`
   if [ -z "$startpid" ]
   then
      echo "threatin failed to start"
      exit
   else
      echo "threatin started with pid $startpid"
      exit
   fi
}

do_stop()
{
   stoppid=`pgrep -f threatin-agent.py`
   
   if [ -z "$stoppid" ]
   then
      echo "threatin is not currently cunning."
   else
      kill $stoppid
      echo "threatin has stopped"
   fi
}

do_status()
{
   threatinpid=`pgrep -f threatin-agent.py`
   if [ -z "$threatinpid" ]
   then
        echo "threatin is not currently running"
        exit
   else
        echo "threatin running with pid $threatinpid"
   fi
}

case "$1" in
   start)
     do_start
     ;;
   stop)
     do_stop
     ;;
   status)
     do_status
     ;;
   restart)
     do_stop
     do_start
     ;;
esac

exit 0
