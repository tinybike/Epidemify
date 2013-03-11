#!/usr/bin/env python
"""
RSS article data miner.

(c) Jack Peterson (jack@tinybike.net), 3/10/2013
"""

from __future__ import division
import MySQLdb
import re
import sys

def main():
	# Set up topic-word association lists
	sick_words = [
		'ailing', 'bedridden', 'debilitate', 'disease', 'fever', 
		'feverish', 'hospitalize', 'ill', 'illness', 'incurable', 
		'infect', 'unhealthy', 'unwell', 'debilitated', 'diseased',
		'infected', 'hospitalized', 'hospitalization', 'sick',
		'sickness', 'sickly',
	]

	# Connect to MySQL database "Epidemify"
	db = MySQLdb.connect(host='localhost', user='epidemician',
						passwd='funcrusherplus', db='Epidemify')
	cur = db.cursor()
	cur.connection.autocommit(True)

	# Get city names and grid coordinates from database
	# For testing, limit to U.S. cities
	search_city = 'Los Angeles'
	print 'Fetching test country code for ' + search_city + '...'
	sql = (
		'SELECT DISTINCT country_id FROM cities '
		'WHERE name = "' + search_city + '";'
	)
	cur.execute(sql)
	country_id = cur.fetchall()[0][0]
	
	# Need to get rid of small-pop cities with redundant names...
	print 'Fetching all cities with country code ' + str(country_id) + '...'
	city = {}
	sql = (
		'SELECT id, name FROM cities '
		'WHERE country_id = ' + str(country_id) + ' AND '
		'(name = "Los Angeles" OR name = "San Francisco"'
		'OR name = "Pensacola" OR name = "Albuquerque"'
		'OR name = "New Orleans" OR name = "Kansas City");'
	)
	cur.execute(sql)
	print str(cur.rowcount) + ' cities found.'
	for row in cur.fetchall():
		city[row[0]] = {'name': row[1], 'sick_words': 0}
	
	# Fetch all RSS-linked articles from database which were updated
	# within the last 5 days
	print 'Fetching all articles updated in the last 5 days...'
	sql = (
		'SELECT title, article FROM rss_data '
		'WHERE updated > DATE_SUB(NOW(), INTERVAL 5 DAY);'
	)
	cur.execute(sql)
	num_articles = cur.rowcount
	sql_results = cur.fetchall()
	title = [row[0] for row in sql_results]
	article = [row[1] for row in sql_results]

	# Set up one big regex for sick words
	print 'Setting up regex...'
	sick_patterns = [r'\b%s\b' % re.escape(s.strip()) for s in sick_words]
	sick_channel = re.compile('|'.join(sick_patterns))

	# Find the occurrences of sick words and city names in each article
	print 'Analyzing article text...'
	for i, a in enumerate(article):
		# Visual progress indicator
		sys.stdout.write('.')
		if not i % 10:
			print

		# Clean up article text a little
		text = a.replace('\t', '').replace('\n', '').replace('\r', '')
		
		# Search the article for city names
		for city_id in city.keys():
			city_pattern = r'\b%s\b' % re.escape(city[city_id]['name'].strip())
			city_found = re.findall(city_pattern, text)
			if city_found and city_found[0]:
				# Increment the sick word counts of any cities with their
				# names found in the article
				num_sick_words = len(re.findall(sick_channel, text.lower()))
				if num_sick_words:
					print city[city_id]['name'] + ': ' + str(num_sick_words)
					city[city_id]['sick_words'] += num_sick_words
		
	
	# Write results to database
	print 'Writing results to database...'
	for city_id in city.keys():
		sql = (
			'INSERT INTO city_sick_counts VALUES (%i, %i);' 
			% (city_id, city[city_id]['sick_words'])
		)
		cur.execute(sql)

	# Close database
	cur.close()
	db.close()
	print 'Done.'
	
if __name__ == '__main__':
	main()
