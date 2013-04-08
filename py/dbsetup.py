#!/usr/bin/env python
"""
Basic setup queries for Epidemify MySQL backend.

(c) Jack Peterson (jack@tinybike.net), 3/10/2013
"""

import MySQLdb
import csv

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

sql = [
	(
		'CREATE TABLE IF NOT EXISTS users ('
		'username VARCHAR(25),'
		'password TEXT,'
		'firstname TEXT,'
		'lastname TEXT,'
		'email TEXT,'
		'joined DATETIME,'
		'PRIMARY KEY(username)'
		') ENGINE=InnoDB;'
	),
	(
		'CREATE TABLE IF NOT EXISTS friends ('
		'user1 VARCHAR(25),'
		'user2 VARCHAR(25),'
		'joined DATETIME'
		') ENGINE=InnoDB;'
	),
	(
		'CREATE TABLE IF NOT EXISTS sick ('
		'sick_id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,'
		'username VARCHAR(25),'
		'lat DECIMAL(11,7),'
		'lng DECIMAL(11,7),'
		'sickname TEXT,'
		'sicktime DATETIME,'
		'PRIMARY KEY(sick_id)'
		') ENGINE=InnoDB;'
	),
	(
		'CREATE TABLE IF NOT EXISTS rss_data ('
		'id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,'
		'link TEXT,'
		'title TEXT,'
		'summary TEXT,'
		'updated DATETIME,'
		'article TEXT,'
		'PRIMARY KEY(id)'
		') ENGINE=InnoDB;'
	),
	(
		'CREATE TABLE IF NOT EXISTS cities ('
		'id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,'
		'name VARCHAR(100),'
		'latitude DECIMAL(7,3),'
		'longitude DECIMAL(7,3),'
		'country_id INT(10) UNSIGNED,'
		'region_id INT(10) UNSIGNED,'
		'timezone VARCHAR(10),'
		'code CHAR(4),'
		'PRIMARY KEY(id)'
		') ENGINE=InnoDB;'
	),
	(
		'CREATE TABLE IF NOT EXISTS city_sick_counts ('
		'city_id INT(10) UNSIGNED,'
		'sick_words INT(10) UNSIGNED,'
		'written DATETIME'
		') ENGINE=InnoDB;'
	),
	(
		'CREATE TABLE IF NOT EXISTS states ('
		'id CHAR(2),'
		'name VARCHAR(100),'
		'latitude DECIMAL(7,3),'
		'longitude DECIMAL(7,3),'
		'PRIMARY KEY(id)'
		') ENGINE=InnoDB;'
	),
	(
		'CREATE TABLE IF NOT EXISTS state_sick_counts ('
		'state_id CHAR(2),'
		'sick_words INT(10) UNSIGNED,'
		'written DATETIME'
		') ENGINE=InnoDB;'
	),
	(
		'CREATE TABLE IF NOT EXISTS populations ('
		'name VARCHAR(100),'
		'region_id INT(10) UNSIGNED,'
		'division_id INT(10) UNSIGNED,'
		'pop_2010 INT(10) UNSIGNED'
		') ENGINE=InnoDB;'
	),
]
	
for query in sql:
	cur.execute(query)
	
cur.close()
db.close()
