#!/usr/bin/env python
"""
RSS article data miner.

(c) Jack Peterson (jack@tinybike.net), 3/10/2013
"""

from __future__ import division
import MySQLdb
import re

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
	city = {}
	cur.execute('SELECT id, name FROM cities;')
	for row in cur.fetchall():
		city[row[0]] = {'name': row[1], 'sick_words': 0}
	
	# Fetch all RSS-linked articles from database which were updated
	# within the last 3 days
	sql = (
		'SELECT article FROM rss_data '
		'WHERE updated > DATE_SUB(NOW(), INTERVAL 3 DAY);'
	)
	cur.execute(sql)
	num_articles = cur.rowcount
	article = [a[0] for a in cur.fetchall()]

	# Set up one big regex for sick words
	sick_patterns = [r'\b%s\b' % re.escape(s.strip()) for s in sick_words]
	sick_channel = re.compile('|'.join(sick_patterns))

	# Find the occurrences of sick words and city names in each article
	for i, a in enumerate(article):
		# Clean up article text a little
		text = a.replace('\t', '').replace('\n', '').replace('\r', '')

		# Find and count up any sick words in the article
		num_sick_words = len(re.findall(sick_channel, text.lower()))
	
		# Increment the sick word counts of any cities with their
		# names found in the article
		for city_id in city.keys():
			city_pattern = r'\b%s\b' % re.escape(city[city_id]['name'].strip())
			city_found = re.findall(city_pattern, text)
			if city_found:
				city[city_id]['sick_words'] += num_sick_words
		
	# Write results to database
	for city_id in city.keys():
		sql = (
			'INSERT INTO city_sick_counts VALUES (%i, %i);' 
			% (city_id, city[city_id]['sick_words'])
		)
		cur.execute(sql)

	# Close database
	cur.close()
	db.close()
	
if __name__ == '__main__':
	main()
