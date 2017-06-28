#!/usr/bin/python

# Python imports
import logging
import logging.config
import threading
import subprocess
import re
import sys
import time
import ast

# Custom imports
import taHelper

## Global variables
# Set up logging files
logging.config.fileConfig('/opt/scripts/THREATIN/threat-agent/etc/taLogging.conf')
logger = logging.getLogger('threatAgent.py')

# Set directories for threat agent configs
main_dir = ('/opt/scripts/THREATIN/threat-agent/')
conf_dir = ('/opt/scripts/THREATIN/threat-agent/etc/')
status_dir = ('/opt/scripts/THREATIN/threat-agent/status/')
plugin_dir = ('/opt/scripts/THREATIN/threat-agent/plugins/')


# Handle creation of threads for agent checks
class SpawnAgent(threading.Thread):
	
	def __init__(self, plug_info):
		
		self.plug_name = plug_info['name']
		self.path = plug_info['path']
		self.freq = plug_info['freq']
		self.cat = plug_info['category']
		threading.Thread.__init__(self)

	def run(self):
	
		while True:
			
			logger.info("Requesting check of plugin " + self.path)

			# build subprocess command to execute
			script_path = plugin_dir + self.path
			proc_out = ''
			results = []

			# execute command
			try:
				proc_out = subprocess.check_output([script_path])
				logger.info('Script executed successfully: ' + script_path)
			except subprocess.CalledProcessError as e:
				logger.error('Script exited with return code ' + str(e.returncode) + ': ' + script_path + ': ' + e.output.strip())
				sys.exit(2)
	
			try:
				results = ast.literal_eval(proc_out)
			except:
				logger.error('Problem evaluating data from script: ' + script_path)
				logger.error('Check that output of ' + script_path + ' is in python readable format.')
				sys.exit(2)

			if results:
				for item in results:
					item_str = str(item['info'])
					print 'inserting item: \n' + item_str
					taHelper.insertThreat(item['date'], self.plug_name, self.cat, item_str)

			# Wait x seconds before checking again
			time.sleep(self.freq)


# Read config file defining plugins and return as a list
def read_config():

	try:
		# read in config file that defines plugins to check
		with open(conf_dir+'ta.conf') as f:
			lines = f.readlines()
	except FileNotFoundError:
		logger.critical('agents.conf file does not exist in ' + conf_dir)
	except Exception, why: 
		logger.critical("Reading config failed: %s" % why)

	# clean the input from agents.conf - ensure first character of line is letter
	valid_lines = []
	for line in lines:
		if re.match("^[A-Za-z]", line):
			valid_lines.append(line)

	# parse each line of config, put fields into dict, add dict to list
	final = []
	for plug in valid_lines:
		d_fields = plug.split(';')
		c_fields = [f.strip() for f in d_fields]

		if len(c_fields) != 4:
			logger.error('Missing fields when parsing line of ta.conf: ' + valid_lines)
			sys.exit(1)

		name = c_fields[0]
		cat = c_fields[1]
		path = c_fields[2]
		freq = c_fields[3]
		try:
			# frequency is in minutes
			freq = int(c_fields[3]) # * 60
		except:
			logger.error('Problem casting frequency to int. Check ta.conf values. Defaulting to 30 minutes.')
			freq = 30

		d = {'name' : name, 'category' : cat, 'path' : path, 'freq' : freq}
		final.append(d)

	return final


if __name__ == "__main__":

	# Spawn threads to handle agent checks (1 thread per agent)
	plugins = read_config()
	try:
		for plugin in plugins:
			agentThread = SpawnAgent(plugin)
			agentThread.start()
	except Exception, why:
		logger.critical("Thread failed: %s" % why)
		sys.exit(1)
