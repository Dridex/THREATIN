#!/bin/bash
# Execute from root directory of THREATIN

if [ "$EUID" -ne 0 ]
then 
	echo "Please run as root"
	exit
fi

echo "Checking version of python..."
pv=`python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))' | grep 2.7`
if [ -z $pv ]; then
   echo "Python 2.7 not installed or not default... please install python2.7"
   exit
else
   echo "Python 2.7 installed and default. Continuing."
fi

echo "Installing necessary packages..."
apt-get -y install mysql-common
apt-get -y install python-pip
pip install mysql-connector-python-rf

# create directories
mkdir -p /opt/scripts/THREATIN/threat-agent/logs
mkdir -p /opt/scripts/THREATIN/threat-agent/plugins
mkdir -p /opt/scripts/THREATIN/threat-agent/etc

echo "Copying files..."
cp ./threat-agent.py /opt/scripts/THREATIN/threat-agent/
chmod 744 /opt/scripts/THREATIN/threat-agent/threat-agent.py
cp ./etc/ta.conf /opt/scripts/THREATIN/threat-agent/etc/
chmod 644 /opt/scripts/THREATIN/threat-agent/etc/ta.conf
cp ./etc/taLogging.conf /opt/scripts/THREATIN/threat-agent/etc/
chmod 644 /opt/scripts/THREATIN/threat-agent/etc/taLogging.conf
touch /opt/scripts/THREATIN/threat-agent/logs/ta.log
chmod 664  /opt/scripts/THREATIN/threat-agent/logs/ta.log
cp ./startup/threatin-init-script.sh /etc/init.d/threat-agent
chmod 755 /etc/init.d/threat-agent
cp ./taHelper.py /opt/scripts/THREATIN/threat-agent/

# Copy the entire plugins folder
plugin_dir=./plugins
for entry in "$plugin_dir"/*
do
   cp -r $entry /opt/scripts/THREATIN/threat-agent/plugins/
done
chmod 744 /opt/scripts/THREATIN/threat-agent/plugins/*
echo "Complete!"

# create system user
echo "Creating threatin user..."
useradd -s /bin/false -M threatin
chown -R threatin. /opt/scripts/THREATIN/
usermod -d /opt/scripts/THREATIN threatin

# Check that mysql is installed 
MYSQL=`which mysql`

if [ "$MYSQL" ]
then
    echo "mysql installed, continuing..."
else
    echo "mysql not installed! Exiting."
	exit 1
fi

# Make sure mysql is running
service mysql start

# setup database
# create random password
PASSWDDB="$(openssl rand -base64 12)"

# database name and username
MAINDB="threatin"

# read the root mysql database password securely
echo "Please enter root user MySQL password."
stty_orig=`stty -g` # save original terminal setting.
stty -echo          # turn-off echoing.
read rootpasswd     # read the password
stty $stty_orig     # restore terminal setting.

mysql -uroot -p${rootpasswd} -e "CREATE DATABASE ${MAINDB} /*\!40100 DEFAULT CHARACTER SET utf8 */;"

exit_status=$?
if [ $exit_status -ne 0 ]; then
    echo "Incorrect mysql root password. Aborting."
	exit
fi

mysql -uroot -p${rootpasswd} -e "CREATE USER '${MAINDB}'@'%' IDENTIFIED BY PASSWORD '${PASSWDDB}';"
mysql -uroot -p${rootpasswd} -e "GRANT ALL PRIVILEGES ON ${MAINDB}.* TO '${MAINDB}'@'%';"
mysql -uroot -p${rootpasswd} -e "FLUSH PRIVILEGES;"
mysql -uroot -p${rootpasswd} -e "USE threatin; CREATE TABLE threats (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
timestamp DATETIME,
source VARCHAR(30),
category VARCHAR(30),
info VARCHAR(2000));"

# change the threatin user's password
echo "Please enter a new password for the threatin mysql user."
stty_orig=`stty -g` # save original terminal setting.
stty -echo          # turn-off echoing.
read newpass        # read the password
stty $stty_orig     # restore terminal setting.
mysql -uroot -p${rootpasswd} -e "SET PASSWORD FOR 'threatin'@'%' = PASSWORD('${newpass}');"

echo "Database created."
echo "THREATIN threat agent installed to /opt/scripts/THREATIN/threat-agent"
