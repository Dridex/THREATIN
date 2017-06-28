#!/usr/bin/python

# Python import
import requests
import json
import logging
import sys
import os.path
import datetime

# Personal import
import hibpScrape

logpath = '/opt/scripts/THREATIN/threat-agent/logs/'
logfile = 'hibp.log'
logfull = logpath+logfile

def returnData():

	# Set up logging
	if not os.path.exists(logpath):
		os.makedirs(logpath)
	if not os.path.exists(logfull):
		open(logfull, 'a').close()

	logging.basicConfig(filename=logfull,level=logging.DEBUG,format='%(asctime)s %(message)s')

	returnList = []

	os.chdir('/opt/scripts/THREATIN/threat-agent/plugins/hibp/')
	pwnfile = 'pwn.txt'
	pwnpath = pwnfile
	#if not os.path.isfile(pwnpath)
	#	logging.warning('pwn.txt not found, creating new file: ' + pwnpath)
	#	pwnfile = open(pwnpath, "w")
	#	r = requests.get('https://haveibeenpwned.com/api/v2/breaches')
	#	if not r.status_code == 200:
	#		logging.error('Problem with request, exiting.')
	#		sys.exit(1)
	#	pwnlist = r.json()
	#	for pwn in pwnlist:
	#		title = pwn['Name'].encode('utf-8') 
	#		pwnfile.write(title + '\n');
	#	pwnfile.close()
	#	returnList.append('PASS')
	#else: 
	
	pwnfile = open(pwnpath, "a+")
	pwnfile.seek(0)
	currentlist = pwnfile.readlines()	
	cliststrip = []
	for item in currentlist:	
		cliststrip.append(item.strip())
	r = requests.get('https://haveibeenpwned.com/api/v2/breaches')
	if not r.status_code == 200:
		logging.error('Problem with request, exiting.')
		sys.exit(1)
	pwnlist = r.json()
	newlist = []
	for pwn in pwnlist:
		newlist.append(pwn['Name'].encode('utf-8'))

	c = set(cliststrip)
	n = set(newlist)
	newbreach = list(n - c)

	if newbreach:
		logging.info('New breach(es)! Writing to file...')
		for item in newbreach:
			pwnfile.write(item + '\n');
		pwnfile.close()
	else:
		logging.info('No change.')

	pwnedAccounts = hibpScrape.scrapeTotal()

	for site in newbreach:
		for pwn in pwnlist:
			if pwn['Name'] == site:
				temp_d = {'Name' : site, 'Domain' : str(pwn['Domain']), 'Size' : str(pwn['PwnCount']), 'Description' : str(pwn['Description'].encode('utf-8'))}
				returnList.append(temp_d)

	#if returnList != []:	
	#	with open(pwnpath) as c:
	#		pwncount = sum(1 for _ in c)
	#	temp_t = {'total_breaches' : str(pwncount), 'total_accounts' : str(pwnedAccounts)}
	#	returnList.append(temp_t)

	return returnList
	
if __name__ == '__main__':

	# Script needs to return a list of items (empty list if nothing new) one or more
	# Each item will be a new row on the threatin page

	# Format needs to be a datetime string, as well as data for the 'info' field in a list
	# Each item in the list will be put as a new line in the info field
	RD = returnData()
	threatinList = []

	# No new results
	if RD == []:
		print []
	# Writing file for first time
	elif RD[0] == 'PASS':
		print []
	# New results
	else:
		for br in RD:
			threatinList.append({'date' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'info' : ['Domain: ' + br['Domain'], 'Size: ' + br['Size'], 'Description: ' + br['Description']]})
		print threatinList
