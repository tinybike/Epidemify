#!/usr/bin/env python
"""
State/regional population table setup.

(c) Jack Peterson (jack@tinybike.net), 4/7/2013
"""

import MySQLdb
import csv

def pop_table_setup():
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
	with open('../data/NST_EST2012_ALLDATA.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for i, row in enumerate(reader):
			if i == 0:
				continue
			sqldict = {
				'region': row[1],
				'division': row[2],
				'name': db.escape_string(row[4]),
				'population': row[5],
			}

			sql = (
				'INSERT INTO populations '
				'(name, region_id, division_id, pop_2010) '
				'VALUES ('
				'"%(name)s", %(region)s, %(division)s, %(population)s);' 
				% sqldict
			).replace('-1', 'NULL')

			cur.execute(sql)

	# Create index
	cur.execute('CREATE INDEX name_index ON populations (name);')

	# Close database
	cur.close()
	db.close()

if __name__ == '__main__':
	pop_table_setup()