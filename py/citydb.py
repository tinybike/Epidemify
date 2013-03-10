#!/usr/bin/env python
"""
City table setup from GeoWorldMap file.

(c) Jack Peterson (jack@tinybike.net), 3/10/2013
"""

import MySQLdb
import csv

# Connect to MySQL database "Epidemify"
db = MySQLdb.connect(host='localhost', user='epidemician',
					 passwd='funcrusherplus', db='Epidemify')
cur = db.cursor()
cur.connection.autocommit(True)

# Get city names and grid coordinates from flat file (GeoWorldMap)
with open('/var/www/htdocs/Epidemify/data/cities.txt', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for i, row in enumerate(reader):
		if i == 0:
			continue
		sqldict = {
			'name': db.escape_string(row[3]),
			'latitude': row[4],
			'longitude': row[5],
			'timezone': row[6],
			'code': row[8],
		}

		sql = (
			'INSERT INTO cities '
			'(name, latitude, longitude, timezone, code) '
		    'VALUES '
			'("%(name)s", "%(latitude)s", "%(longitude)s", "%(timezone)s"'
			', "%(code)s");' % sqldict
		).replace('"NULL"', 'NULL')

		cur.execute(sql)

# Close database
cur.close()
db.close()
