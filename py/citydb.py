#!/usr/bin/env python
"""
City table setup from GeoWorldMap file.

(c) Jack Peterson (jack@tinybike.net), 3/10/2013
"""

import MySQLdb
import csv

def city_table_setup():
	'''Set up MySQL table of city names, region, coordinates, etc. from flat
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

	# Get city names and grid coordinates from flat file (GeoWorldMap)
	with open('../data/cities.txt', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for i, row in enumerate(reader):
			if i == 0:
				continue
			sqldict = {
				'country_id': row[1],
				'region_id': row[2],
				'name': db.escape_string(row[3]),
				'latitude': row[4],
				'longitude': row[5],
				'timezone': row[6],
				'code': row[8],
			}

			sql = (
				'INSERT INTO cities '
				'(name, latitude, longitude, country_id, region_id, timezone, '
				'code) '
				'VALUES ('
				'"%(name)s", "%(latitude)s", "%(longitude)s", "%(country_id)s"'
				', "%(region_id)s", "%(timezone)s", "%(code)s");' % sqldict
			).replace('"NULL"', 'NULL')

			cur.execute(sql)

	# Create country ID index
	cur.execute('CREATE INDEX country_index ON cities (country_id);')
	cur.execute('CREATE INDEX name_index ON cities (name);')

	# Close database
	cur.close()
	db.close()

if __name__ == '__main__':
	city_table_setup()
