#!/bin/bash
# Execute from root directory of THREATIN

if [ "$EUID" -ne 0 ]
then 
	echo "Please run as root"
	exit
fi

echo "Checking threat agent installation..."
if [ -d "/opt/scripts/THREATIN/threat-agent" ]; then
   echo "Threat Agent already installed. Continuing."
else
   echo "Please install the THREATIN threat agent before installing the web agent."
   exit
fi

mkdir -p /opt/scripts/THREATIN/web-agent/logs
mkdir -p /opt/scripts/THREATIN/web-agent/etc

echo "Copying files..."
cp ./web-agent.py /opt/scripts/THREATIN/web-agent/
chmod 744 /opt/scripts/THREATIN/web-agent/web-agent.py
cp ./etc/waLogging.conf /opt/scripts/THREATIN/web-agent/etc/
chmod 644 /opt/scripts/THREATIN/web-agent/etc/waLogging.conf
touch /opt/scripts/THREATIN/web-agent/logs/wa.log
chmod 664  /opt/scripts/THREATIN/web-agent/logs/wa.log
cp ./startup/webagent-init-script.sh /etc/init.d/web-agent
chmod 755 /etc/init.d/web-agent
cp ./waHelper.py /opt/scripts/THREATIN/web-agent/
chmod 644 /opt/scripts/THREATIN/web-agent/waHelper.py
cp -r ./www /opt/scripts/THREATIN/web-agent/
chmod -R 644 /opt/scripts/THREATIN/web-agent/www/

chown -R threatin. /opt/scripts/THREATIN/web-agent/

# Make sure mysql is running
service mysql start

echo "THREATIN web agent installed to /opt/scripts/THREATIN/web-agent"
