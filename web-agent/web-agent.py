#!/usr/bin/env python

# Python imports
import os
import sys
import logging
import logging.config
import time
import ast

# Custom imports
import waHelper

logging.config.fileConfig('/opt/scripts/THREATIN/web-agent/etc/waLogging.conf')
logger = logging.getLogger('webAgent.py')
web_dir = '/opt/scripts/THREATIN/web-agent/www/'


def monitor():

	while True:

		# Get top 100 rows from threats table
		try:
			results = waHelper.readThreats()
		except Exception, why:
			logger.error("Unable to get threats from database: %s" % why)

		# update web page with database results
		updateWeb(results)

		time.sleep(30)


# update web page with database results
def updateWeb(results):

	# print results[0][0]

	table_str = ""
	for result in results:
		table_str += '\n<tr>'

		date_obj = result[1]
		date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")

		table_str += '\n<td>' + date_str + '</td>'
		table_str += '\n<td>' + result[3] + '</td>'
		table_str += '\n<td>' + result[2] + '</td>'

		info_str = result[4]
		info = ast.literal_eval(info_str)
		final_str = ""
		for item in info:
			final_str += item + '<br>'

		table_str += '\n<td>' + final_str.decode('utf-8') + '</td>'
		table_str += '\n</tr>'

	# print table_str

	html_file = 'index.html'
	path = web_dir + html_file
	index = open(path,'w')
	
	message = """<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>THREATIN</title>

    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">

    <!-- Custom CSS -->
    <style>
    body {
        padding-top: 70px;
        /* Required padding for .navbar-fixed-top. Remove if using .navbar-static-top. Change if height of navigation changes. */
    }
    </style>

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <!-- Navigation -->
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">THREATIN</a>
            </div>
            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav">
<!--                <li>
                        <a href="#">About</a>
                    </li>
                    <li>
                        <a href="#">Services</a>
                    </li>
                    <li>
                        <a href="#">Contact</a>
                    </li>-->
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

    <!-- Page Content -->
    <div class="container">

        <!--<div class="row">-->
            <!--<div class="col-lg-12 text-center">
                <h1>A Bootstrap Starter Template</h1>
                <p class="lead">Complete with pre-defined file paths that you won't have to change!!</p>
                <ul class="list-unstyled">
                    <li>Bootstrap v3.3.7</li>
                    <li>jQuery v1.11.1</li>
                </ul>-->

                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>DateTime</th>
                      <th>Category</th>
                      <th>Source</th>
                      <th>Info</th>
                    </tr>
                  </thead>
                  <tbody>

""" + table_str + """

                  </tbody>
                </table>

            <!--</div>-->
        <!--</div>-->
        <!-- /.row -->

    </div>
    <!-- /.container -->

    <!-- jQuery Version 1.11.1 -->
    <script src="js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>

</body>

</html>"""

	final_message = message.encode('utf-8')	
	index.write(final_message)
	index.close()
	print 'Web page written.'


    
if __name__ == '__main__':

	logger.info("Web agent script running...")
	monitor()	
