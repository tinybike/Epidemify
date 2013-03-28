#!/usr/bin/env python
"""
State table setup.

(c) Jack Peterson (jack@tinybike.net), 3/28/2013
"""

import MySQLdb
import csv

def city_table_setup():
	'''Set up MySQL table of U.S. states and centroid coordinates from flat
	file.
	'''
	# Connect to MySQL database "Epidemify"
	with open('dbparams.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		params = list(reader)[0]			
	db = MySQLdb.connect(
		host=params[0], 
		user=params[1],
		passwd=params[2], 
		db=params[3]
	)
	cur = db.cursor()
	cur.connection.autocommit(True)

	# Get state names and (center) grid coordinates from flat file
	with open('../data/state_latlon.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for i, row in enumerate(reader):
			if i == 0:
				continue
			sqldict = {
				'name': db.escape_string(row[0]),
				'latitude': row[1],
				'longitude': row[2],
			}

			sql = (
				'INSERT INTO states '
				'(name, latitude, longitude) '
				'VALUES ('
				'"%(name)s", "%(latitude)s", "%(longitude)s");' 
				% sqldict
			).replace('"NULL"', 'NULL')

			cur.execute(sql)

	# Create index
	cur.execute('CREATE INDEX name_index ON cities (name);')

	# Close database
	cur.close()
	db.close()

if __name__ == '__main__':
	city_table_setup()
