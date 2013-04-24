#!/usr/bin/env python
"""
RSS article data miner.

(c) Jack Peterson (jack@tinybike.net), 3/10/2013
"""

from __future__ import division
import MySQLdb
import re
import sys
import time
import csv

def rssminer():
	'''Mines the full text of news articles for association with
	a list of 'sick' words -- ailing, ill, diseased, etc. -- and
	also for each of a table of cities.  My hypothesis is that
	sick words in news articles is a reasonable indicator of
	disease breakouts at cities whose names are also contained in
	that article's text.  (Initial plausibility will be checked
	against CDC data.)  The number of sick words per city is time-
	stamped and saved in a MySQL database.
	'''
	# Set up sick-word association list
	sick_words = [
		'ailing', 'bedridden', 'debilitate', 'disease', 'fever', 
		'feverish', 'hospitalize', 'ill', 'illness', 'incurable', 
		'infect', 'unhealthy', 'unwell', 'debilitated', 'diseased',
		'infected', 'hospitalized', 'hospitalization', 'sick',
		'sickness', 'sickly',
	]

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

	# Get city names and grid coordinates from database
	# For testing, limit to U.S. cities
	#search_city = 'Los Angeles'
	#print 'Fetching test country code for %s...' % search_city
	#sql = (
	#	'SELECT DISTINCT country_id FROM cities '
	#	'WHERE name = "%s";' % search_city
	#)
	#cur.execute(sql)
	#country_id = cur.fetchall()[0][0]
	
	#print 'Fetching cities with country code %i...' % country_id
	#city = {}
	#sql = (
	#	'SELECT MAX(id), name FROM cities '
	#	'WHERE country_id = %i GROUP BY name LIMIT 500 '
	#	'UNION '
	#	'SELECT id, name FROM cities '
	#	'WHERE '
	#	'(name = "Los Angeles" OR name = "San Francisco"'
	#	'OR name = "Pensacola" OR name = "Albuquerque"'
	#	'OR name = "New Orleans"'
	#	'OR name = "Salt Lake City");'
	#	% country_id
	#)
	#cur.execute(sql)
	#print '%i cities found.' % cur.rowcount
	
	# Cities have too many duplicates + names that double as personal names;
	# try using state names instead!
	city = {}
	cur.execute('SELECT id, name FROM states;')
	for row in cur.fetchall():
		city[row[0]] = {'name': row[1], 'sick_words': 0}
	
	# Fetch all RSS-linked articles from database which were updated
	# within the last 5 days
	print 'Fetching all articles updated in the last 30 days...'
	#sql = (
	#	'SELECT title, article FROM rss_data '
	#	'WHERE updated > DATE_SUB(NOW(), INTERVAL 30 DAY);'
	#)
	#sql = (
	#	'SELECT r.title, r.article FROM rss_data r '
	#	'WHERE r.updated = ('
	#	'	SELECT MAX(updated) FROM rss_data '
	#	'	WHERE title = r.title'
	#	') GROUP BY r.title;'
	#)
	sql = (
		'SELECT title, article FROM rss_data GROUP BY title;'
	)
	cur.execute(sql)
	num_articles = cur.rowcount
	sql_results = cur.fetchall()
	title = [row[0] for row in sql_results]
	article = [row[1] for row in sql_results]

	# Set up one big regex for sick words
	sick_patterns = [r'\b%s\b' % re.escape(s.strip()) for s in sick_words]
	sick_channel = re.compile('|'.join(sick_patterns))

	# Find the occurrences of sick words and city names in each article
	print 'Analyzing article text...'
	pbar_width = 80
	sys.stdout.write('[%s]' % (' ' * pbar_width))
	sys.stdout.flush()
	sys.stdout.write('\b' * (pbar_width + 1))
	pbar_extend = int(len(article)/pbar_width) + 1
	for i, a in enumerate(article):
		# Clean up article text a little
		if a:
			text = a.replace('\t', '').replace('\n', '').replace('\r', '')

			# Search the article for city names
			for city_id in city.keys():
				city_pattern = r'\b%s\b' % \
					re.escape(city[city_id]['name'].strip())
				city_found = re.findall(city_pattern, text)

				# Increment the sick word counts of any cities with their
				# names found in the article
				if city_found and city_found[0]:
					num_sick_words = \
						len(re.findall(sick_channel, text.lower()))
					if num_sick_words:
						city[city_id]['sick_words'] += num_sick_words
						
		# Update visual progress indicator
		if not i % pbar_extend:
			sys.stdout.write('#')
			sys.stdout.flush()
			
	sys.stdout.write('\n')
	for city_id in city.keys():
		if city[city_id]['sick_words']:
			print '%s: %i' % (
				city[city_id]['name'], city[city_id]['sick_words']
			)
	
	# Write results to database
	print 'Writing results to database...'
	for city_id in city.keys():
		sql = (
			'INSERT INTO state_sick_counts VALUES ("%s", %i, NOW());' 
			% (city_id, city[city_id]['sick_words'])
		)
		cur.execute(sql)

	# Close database
	cur.close()
	db.close()
	print 'Done.'
	
if __name__ == '__main__':
	rssminer()