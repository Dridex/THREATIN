#!/bin/bash
# Execute from root directory of THREATIN

if [ "$EUID" -ne 0 ]
then 
	echo "Please run as root"
	exit
fi

echo "Copying files..."
cp ./threat-agent.py /opt/scripts/THREATIN/threat-agent/
chmod 744 /opt/scripts/THREATIN/threat-agent/threat-agent.py
cp ./etc/ta.conf /opt/scripts/THREATIN/threat-agent/etc/
chmod 644 /opt/scripts/THREATIN/threat-agent/etc/ta.conf
cp ./etc/taLogging.conf /opt/scripts/THREATIN/threat-agent/etc/
chmod 644 /opt/scripts/THREATIN/threat-agent/etc/taLogging.conf
touch /opt/scripts/THREATIN/threat-agent/logs/ta.log
chown threatin. /opt/scripts/THREATIN/threat-agent/logs/ta.log
chmod 664  /opt/scripts/THREATIN/threat-agent/logs/ta.log
cp ./startup/threatin-init-script.sh /etc/init.d/threatin
chmod 755 /etc/init.d/threatin
cp ./taHelper.py /opt/scripts/THREATIN/threat-agent/

# Copy the entire plugins folder
plugin_dir=./plugins
for entry in "$plugin_dir"/*
do
   cp -r $entry /opt/scripts/THREATIN/threat-agent/plugins/
done
chmod 744 /opt/scripts/THREATIN/threat-agent/plugins/*
echo "Complete!"
