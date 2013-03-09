"""
Basic setup queries for Epidemify MySQL backend.

(c) Jack Peterson (jack@tinybike.net), 3/8/2013
"""

import MySQLdb

db = MySQLdb.connect(host='localhost', user='epidemician', passwd='funcrusherplus', db='Epidemify')
cursor = db.cursor()

sql = [('CREATE TABLE IF NOT EXISTS users ('
	'username VARCHAR(25),'
	'password TEXT,'
	'firstname TEXT,'
	'lastname TEXT,'
	'email TEXT,'
	'joined DATETIME,'
	'PRIMARY KEY(username)'
	') ENGINE=InnoDB;'),
	('CREATE TABLE IF NOT EXISTS friends ('
	'user1 VARCHAR(25),'
	'user2 VARCHAR(25),'
	'joined DATETIME'
	') ENGINE=InnoDB;'),
	('CREATE TABLE IF NOT EXISTS sick ('
	'sick_id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,'
	'username VARCHAR(25),'
	'lat DECIMAL(11,7),'
	'lng DECIMAL(11,7),'
	'sickname TEXT,'
	'sicktime DATETIME,'
	'PRIMARY KEY(sick_id)'
	') ENGINE=InnoDB;'),
	('CREATE TABLE IF NOT EXISTS rss_data ('
	'link TEXT,'
	'title TEXT,'
	'summary TEXT,'
	'updated DATETIME,'
	'article TEXT'
	') ENGINE=InnoDB;')]
	
for query in sql:
	cursor.execute(query)
	
db.commit()
cursor.close()
db.close()
