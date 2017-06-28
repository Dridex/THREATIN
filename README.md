THREATIN is an open source python script designed to collate threat intelligence information through the use of plugin scripts that gather information from different sources. The motivation for this architecture is that threat intelligence data comes in many forms and formats, so the plugin scripts need to do the hard work of converting the data to a nice format to be passed to the threat agent, which will in turn store the data in a database. An intelligence agent then pulls the data from this database to present in a human-readable way in a webpage.

The format that a plugin needs to return data in for the agent to understand is as follows:<br>
	* The script needs to return a list of items (in python format, to be understood by the agent), where each item in the list will be a new row in the database.<br>
	* Each item of the list will be a python readable dictionary (JSON) that specifies the following three fields:<br>
		- datetime: datetime in the format "YYYY-MM-DD HH:MM:SS" <br>
		- source: simple title for the source of the intel<br>
		- info: general field for the actual intel. Needs to be a list, where each item will be a string representing a new line within the row]<br>
<br>
<br>
INSTALL INSTRUCTIONS:<br>
	1. Run the TREATINSTALL.sh script in the root directory.<br>
	2. Proceed to debug the hell out of it because I won't have tested it enough.<br>
	3. THREATIN is now installed. <br>
