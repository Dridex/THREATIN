#!/usr/bin/python
# Version 1.0
import os
import re
import sys
import logging
import logging.config
import base64
import urllib
import binascii
import StringIO
import time
import datetime

import mysql.connector as mdb

from Crypto.Cipher import AES
from Crypto import Random

os.chdir('/opt/scripts/THREATIN/threat-agent/')
logging.config.fileConfig('/opt/scripts/THREATIN/threat-agent/etc/taLogging.conf')
logger = logging.getLogger('taHelper.py')

## Fill in the mysql threatin password you entered upon install.
mysql_user = 'threatin'
mysql_db = 'threatin'
mysql_pass = ''

def insertThreat(ts, source, category, info):

	mdb_conn = mdb.connect(user=mysql_user, password=mysql_pass, database=mysql_db)
	cursor = mdb_conn.cursor()
	
	try:
		cursor.execute("INSERT INTO threats (timestamp, source, category, info) VALUES (%s,%s,%s,%s)",(ts, source, category, info))
		cursor.close()
		mdb_conn.commit()
		mdb_conn.close()
	except Exception, e:
		logger.error("Error in insertThreat:")
		logger.error(e)
		return 0


# Query the database for a particular service
def queryService(name, args, hostUID):

	try:
		dbconn = pyodbc.connect(connect_string)
		sql = 'SELECT * FROM [Data].[dbo].[AidsService] WHERE [Script] = ? and [HostID] = ? and [Args] = ?'
		cursor = dbconn.execute(sql, (name, hostUID, args))
		results = cursor.fetchall()
		cursor.close()
		dbconn.close()
		return results
	except Exception, e:
		logger.error("Error in queryService:")
		logger.error(e)
		return None


# Set all hosts belonging to a controller to DOWN
def setHostsDown(hostUID):

	sql = 'UPDATE [Data].[dbo].[AidsHost] SET [Status] = ? WHERE ID = ? or ZoneParent = ?'

	try:
		dbconn = pyodbc.connect(connect_string)
		cursor = dbconn.execute(sql, ('DOWN', hostUID, hostUID))
		rowcount = cursor.rowcount
		cursor.close()
		dbconn.commit()
		dbconn.close()
		return rowcount
	except Exception, e:
		logger.error("Error in setHostsDown:")
		logger.error(e)
		return 0


def pkcs7_decode(text, k):
	'''
	Remove the PKCS#7 padding from a text string
	'''
	nl = len(text)
	val = int(binascii.hexlify(text[-1]), 16)

	if val > k:
		raise ValueError('Input is not padded or padding is corrupt')

	l = nl - val
	return text[:l]


def pkcs7_encode(text, k):
	'''
	Pad an input string according to PKCS#7
	'''
	l = len(text)
	output = StringIO.StringIO()
	val = k - (l % k)

	for _ in xrange(val):
		output.write('%02x' % val)

	return text + binascii.unhexlify(output.getvalue())


def encrypt(text):
	key = 'iosje6rioj*#$(WOF"F"G:AD}{``efEF'

	# 16 byte initialization vector
	#iv = '1234567812345678'
	iv =  Random.get_random_bytes(16)
	aes = AES.new(key, AES.MODE_CBC, iv)

	# pad the plain text according to PKCS7
	pad_text = pkcs7_encode(text, 16)
	# encrypt the padding text
	cipher = aes.encrypt(pad_text)
	# base64 encode the cipher text for transport
	enc_cipher = base64.b64encode(iv + cipher)

	return enc_cipher


def decrypt(cipherString):
	key = 'iosje6rioj*#$(WOF"F"G:AD}{``efEF'

	# 16 byte initialization vector
	# iv = '1234567812345678'

	dec_cipher = base64.b64decode(cipherString)

	iv = dec_cipher[:16]
	cipher = dec_cipher[16:]

	aes = AES.new(key, AES.MODE_CBC, iv)

	text = aes.decrypt(cipher)
	upad_text = pkcs7_decode(text, 16)

	return upad_text

