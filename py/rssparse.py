"""
RSS news parser.

(c) Jack Peterson (jack@tinybike.net), 3/8/2013
"""

from __future__ import division
import MySQLdb
import feedparser
import nltk
from mechanize import Browser

db = MySQLdb.connect(host='localhost', user='epidemician', \
					passwd='funcrusherplus', db='Epidemify')
cursor = db.cursor()

br = Browser()
br.set_handle_robots(False)
br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')]

# URL list: (1) FARK, (2) all CNN feeds, (3) page 1 of MSNBC (-sports)
urls = ['http://www.fark.com/fark.rss', \
		'http://rss.cnn.com/rss/cnn_world.rss', \
		'http://rss.cnn.com/rss/cnn_topstories.rss', \
		'http://rss.cnn.com/rss/cnn_us.rss', \
		'http://rss.cnn.com/rss/money_latest.rss', \
		'http://rss.cnn.com/rss/cnn_allpolitics.rss', \
		'http://rss.cnn.com/rss/cnn_crime.rss', \
		'http://rss.cnn.com/rss/cnn_tech.rss', \
		'http://rss.cnn.com/rss/cnn_health.rss', \
		'http://rss.cnn.com/rss/cnn_showbiz.rss', \
		'http://rss.cnn.com/rss/cnn_travel.rss', \
		'http://rss.cnn.com/rss/cnn_living.rss', \
		'http://rss.cnn.com/rss/cnn_freevideo.rss', \
		'http://rss.cnn.com/rss/cnn_studentnews.rss', \
		'http://rss.cnn.com/rss/cnn_mostpopular.rss', \
		'http://rss.cnn.com/rss/cnn_latest.rss', \
		'http://rss.ireport.com/feeds/oncnn.rss', \
		'http://rss.cnn.com/rss/cnn_behindthescenes.rss', \
		'http://news.google.com/news?pz=1&cf=all&ned=us&hl=en&output=rss', \
		'http://rss.msnbc.msn.com/id/3032091/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/20381145/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032524/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032506/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032552/device/rss/rss.xml', \
		'http://rss.nbcsports.msnbc.com/id/3032112/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032071/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3088327/device/rss/rss.xml', \
		'http://www.today.com/id/3032083/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032117/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032122/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032127/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032618/device/rss/rss.xml', \
		'http://www.today.com/id/3032632/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3096433/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/21760355/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032492/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/8884853/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032479/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3032571/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/21657361/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/4429950/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3036013/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3036018/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3036050/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3036033/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3036058/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/3036028/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/13282720/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/21491571/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/21491043/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/28180066/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/49535854/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/41873451/device/rss/rss.xml', \
		'http://rss.msnbc.msn.com/id/49701499/device/rss/rss.xml', \
		'http://rss.nbcsports.msnbc.com/id/3032824/device/rss/rss.xml', \
		'http://rss.nbcsports.msnbc.com/id/28298620/device/rss/rss.xml', \
		'http://rss.nbcsports.msnbc.com/id/3032846/device/rss/rss.xml']

N = len(urls)
fields = ['link', 'title', 'summary', 'updated_parsed']
counter = 0
for url in urls:
	counter += 1
	print str(counter) + ' (' + str(round(counter/N*100**2)/100) + '%) ' + url
	rss = feedparser.parse(url)
	sqldict = {}
	for e in rss.entries:
		for f in fields:
			if f == 'updated_parsed':
				# Convert RSS time to SQL datetime format
				try:
					sqltime = str(e[f].tm_year) + '-' + str(e[f].tm_mon) + '-' \
							+ str(e[f].tm_mday) + ' ' + str(e[f].tm_hour) + ':' \
							+ str(e[f].tm_min) + ':' + str(e[f].tm_sec)
					sqldict['updated'] = sqltime
				except KeyError:
					sqldict[f] = 'NULL'
			else:
				try:
					sqldict[f] = db.escape_string(e[f].encode('UTF-8'))
				except KeyError:
					sqldict[f] = 'NULL'

		# Follow link in link entry then extract text from html
		try:
			print ' -> ' + e.link
			#html = urllib.urlopen(e.link).read()
			html = br.open(e.link).read()
			sqldict['text'] = db.escape_string(nltk.clean_html(html))
		except KeyboardInterrupt:
			raise
		except:
			sqldict['text'] = 'NULL'

		# Write RSS and article data to database
		sql = ('INSERT INTO rss_data VALUES ' \
			   '("%(link)s", "%(title)s", "%(summary)s", "%(updated)s", ' \
			   '"%(text)s");' % sqldict).replace('"NULL"', 'NULL')
		cursor.execute(sql)
		db.commit()

cursor.close()
db.close()
