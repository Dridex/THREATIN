#!/usr/bin/python
# Version 1.0
import os
import logging
import logging.config
import datetime

import mysql.connector as mdb

os.chdir('/opt/scripts/THREATIN/web-agent/')
logging.config.fileConfig('/opt/scripts/THREATIN/web-agent/etc/waLogging.conf')
logger = logging.getLogger('waHelper.py')

## Enter the password you entered upon install
mysql_user = 'threatin'
mysql_db = 'threatin'
mysql_pass = ''


def readThreats():

	mdb_conn = mdb.connect(user=mysql_user, password=mysql_pass, database=mysql_db)
	cursor = mdb_conn.cursor()
	
	try:
		cursor.execute("SELECT * from threats LIMIT 100")
		results = cursor.fetchall()
		mdb_conn.commit()
		mdb_conn.close()
		return results
	except Exception, e:
		logger.error("Error in insertThreat:")
		logger.error(e)
		return None
