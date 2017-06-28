#!/bin/bash
### BEGIN INIT INFO
# Provides: web-agent
# Required-Start: $local_fs
# Required-Stop: $local_fs
# Short-Description: Start and Stop threatin web-agent service
# Description: threatin is a threat intellience platform framework
# Default-Start: start
# Default-Stop: stop
### END INIT INFO

PATH=/bin:/usr/bin:/sbin:/usr/sbin

DESC="threatin web-agent startup script"
NAME=webagent
DAEMON=webagentd

do_start()
{

   service mysql start
   su -s /bin/bash -c '/opt/scripts/THREATIN/web-agent/web-agent.py >/dev/null 2>/dev/null &' threatin
   sleep 2
   startpid=`pgrep -f web-agent.py`
   if [ -z "$startpid" ]
   then
      echo "web agent failed to start"
      exit
   else
      echo "web agent started with pid $startpid"
      exit
   fi
}

do_stop()
{
   stoppid=`pgrep -f web-agent.py`
   
   if [ -z "$stoppid" ]
   then
      echo "web agent is not currently cunning."
   else
      kill $stoppid
      echo "web agent has stopped"
   fi
}

do_status()
{
   threatinpid=`pgrep -f web-agent.py`
   if [ -z "$threatinpid" ]
   then
        echo "web agent is not currently running"
        exit
   else
        echo "web agent running with pid $threatinpid"
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
