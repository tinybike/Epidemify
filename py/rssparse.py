"""
RSS news parser.

(c) Jack Peterson (jack@tinybike.net), 3/8/2013
"""

from __future__ import division
import MySQLdb
import feedparser
import nltk
from mechanize import Browser

# RSS URL list
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
		'http://rss.nbcsports.msnbc.com/id/3032846/device/rss/rss.xml', \
		'http://www.npr.org/rss/rss.php?id=1001', \
		'http://www.npr.org/rss/rss.php?id=100', \
		'http://www.npr.org/rss/rss.php?id=1008', \
		'http://www.npr.org/rss/rss.php?id=1006', \
		'http://www.npr.org/rss/rss.php?id=1007', \
		'http://www.npr.org/rss/rss.php?id=1057', \
		'http://www.npr.org/rss/rss.php?id=1021', \
		'http://www.npr.org/rss/rss.php?id=1012', \
		'http://www.npr.org/rss/rss.php?id=1003', \
		'http://www.npr.org/rss/rss.php?id=1004', \
		'http://www.npr.org/rss/rss.php?id=2', \
		'http://www.npr.org/rss/rss.php?id=37', \
		'http://www.npr.org/rss/rss.php?id=3', \
		'http://www.npr.org/rss/rss.php?id=5', \
		'http://www.npr.org/rss/rss.php?id=13', \
		'http://www.npr.org/rss/rss.php?id=46', \
		'http://www.npr.org/rss/rss.php?id=7', \
		'http://www.npr.org/rss/rss.php?id=10', \
		'http://www.npr.org/rss/rss.php?id=39', \
		'http://www.npr.org/rss/rss.php?id=43', \
		'http://www.npr.org/rss/rss.php?id=1030', \
		'http://www.npr.org/rss/rss.php?id=1013', \
		'http://www.npr.org/rss/rss.php?id=1017', \
		'http://www.npr.org/rss/rss.php?id=1025', \
		'http://www.npr.org/rss/rss.php?id=1053', \
		'http://www.npr.org/rss/rss.php?id=1052', \
		'http://www.npr.org/rss/rss.php?id=1027', \
		'http://www.npr.org/rss/rss.php?id=1022', \
		'http://www.npr.org/rss/rss.php?id=1010', \
		'http://www.npr.org/rss/rss.php?id=1070', \
		'http://www.npr.org/rss/rss.php?id=1020', \
		'http://www.npr.org/rss/rss.php?id=1009', \
		'http://www.npr.org/rss/rss.php?id=1045', \
		'http://www.npr.org/rss/rss.php?id=1039', \
		'http://www.npr.org/rss/rss.php?id=1046', \
		'http://www.npr.org/rss/rss.php?id=1014', \
		'http://www.npr.org/rss/rss.php?id=1018', \
		'http://www.npr.org/rss/rss.php?id=1048', \
		'http://www.npr.org/rss/rss.php?id=1015', \
		'http://www.npr.org/rss/rss.php?id=1016', \
		'http://www.npr.org/rss/rss.php?id=1024', \
		'http://www.npr.org/rss/rss.php?id=1026', \
		'http://www.npr.org/rss/rss.php?id=1055', \
		'http://www.npr.org/rss/rss.php?id=1050', \
		'http://www.npr.org/rss/rss.php?id=1019', \
		'http://www.npr.org/rss/rss.php?id=1047', \
		'http://www.npr.org/rss/rss.php?id=1049', \
		'http://feeds.feedburner.com/cnet/NnTv?format=xml', \
		'http://feeds.foxnews.com/foxnews/latest?format=xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/GlobalHome.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/World.xml', \
		'http://atwar.blogs.nytimes.com/feed/', \
		'http://www.nytimes.com/services/xml/rss/nyt/Africa.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Americas.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Europe.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/MiddleEast.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/US.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Education.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Politics.xml', \
		'http://thelede.blogs.nytimes.com/feed/', \
		'http://www.nytimes.com/services/xml/rss/nyt/NYRegion.xml', \
		'http://cityroom.blogs.nytimes.com/feed/', \
		'http://fort-greene.blogs.nytimes.com/feed', \
		'http://eastvillage.thelocal.nytimes.com/feed/', \
		'http://feeds.nytimes.com/nyt/rss/Business', \
		'http://www.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/GlobalBusiness.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Economy.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/YourMoney.xml', \
		'http://feeds.nytimes.com/nyt/rss/Technology', \
		'http://bits.blogs.nytimes.com/feed/', \
		'http://www.nytimes.com/services/xml/rss/nyt/PersonalTech.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Science.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Environment.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Space.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Health.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Research.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Nutrition.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/HealthCarePolicy.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Views.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/Magazine.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/pop_top.xml', \
		'http://lens.blogs.nytimes.com/feed/', \
		'http://www.nytimes.com/services/xml/rss/nyt/MostViewed.xml', \
		'http://www.nytimes.com/services/xml/rss/nyt/MostShared.xml', \
		'http://nytimes.com/timeswire/feeds/', \
		'http://topics.blogs.nytimes.com/feed', \
		'http://topics.nytimes.com/top/opinion/editorialsandoped/editorials/index.html?rss=1', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news1', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news11', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news2', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news3', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news4', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news55', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news56', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news5', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news6', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news7', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=news20', \
		'http://content.usatoday.com/marketing/rss/rsstrans.aspx?feedId=weather1', \
		'http://www.forbes.com/feeds/popstories.xml', \
		'http://www.forbes.com/real-time/feed2/', \
		'http://www.forbes.com/markets/index.xml', \
		'http://www.forbes.com/europe_news/index.xml', \
		'http://www.forbes.com/asia_news/index.xml', \
		'http://feeds.bbci.co.uk/news/rss.xml', \
		'http://feeds.bbci.co.uk/news/world/rss.xml', \
		'http://feeds.bbci.co.uk/news/uk/rss.xml', \
		'http://feeds.bbci.co.uk/news/business/rss.xml', \
		'http://feeds.bbci.co.uk/news/politics/rss.xml', \
		'http://feeds.bbci.co.uk/news/health/rss.xml', \
		'http://feeds.bbci.co.uk/news/education/rss.xml', \
		'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml', \
		'http://feeds.bbci.co.uk/news/technology/rss.xml', \
		'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml', \
		'http://feeds.bbci.co.uk/news/world/africa/rss.xml', \
		'http://feeds.bbci.co.uk/news/world/asia/rss.xml', \
		'http://feeds.bbci.co.uk/news/world/europe/rss.xml', \
		'http://feeds.bbci.co.uk/news/world/latin_america/rss.xml', \
		'http://feeds.bbci.co.uk/news/world/middle_east/rss.xml', \
		'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml', \
		'http://feeds.bbci.co.uk/news/england/rss.xml', \
		'http://feeds.bbci.co.uk/news/northern_ireland/rss.xml', \
		'http://feeds.bbci.co.uk/news/scotland/rss.xml', \
		'http://feeds.bbci.co.uk/news/wales/rss.xml', \
		'http://www.sciencenews.org/view/feed/name/allrss', \
		'http://www.sciencenews.org/view/feed/type/blog/name/blog_entries.rss', \
		'http://www.sciencenews.org/view/feed/type/column/name/column_entries.rss', \
		'http://www.sciencenews.org/view/feed/type/news/name/articles.rss', \
		'http://www.sciencenews.org/view/feed/label_id/2357/name/Body_%2B_Brain.rss', \
		'http://www.sciencenews.org/view/feed/label_id/2337/name/Environment.rss', \
		'http://www.lloydslist.com/ll/news/?service=rss', \
		'http://www.lloydslist.com/ll/world/africa/?service=rss', \
		'http://www.lloydslist.com/ll/world/asia/?service=rss', \
		'http://www.lloydslist.com/ll/world/c-and-s-america/?service=rss', \
		'http://www.lloydslist.com/ll/world/europe/?service=rss', \
		'http://www.lloydslist.com/ll/world/middle-east/?service=rss', \
		'http://www.lloydslist.com/ll/world/north-america/?service=rss', \
		'http://feeds.abcnews.com/abcnews/topstories', \
		'http://feeds.abcnews.com/abcnews/internationalheadlines', \
		'http://feeds.abcnews.com/abcnews/usheadlines', \
		'http://feeds.abcnews.com/abcnews/politicsheadlines', \
		'http://feeds.abcnews.com/abcnews/healthheadlines', \
		'http://feeds.abcnews.com/abcnews/travelheadlines', \
		'http://feeds.abcnews.com/abcnews/worldnewsheadlines', \
		'http://feeds.abcnews.com/abcnews/2020headlines', \
		'http://feeds.abcnews.com/abcnews/primetimeheadlines', \
		'http://feeds.abcnews.com/abcnews/nightlineheadlines', \
		'http://feeds.abcnews.com/abcnews/gmaheadlines', \
		'http://feeds.abcnews.com/abcnews/thisweekheadlines', \
		'http://feeds.abcnews.com/abcnews/mostreadstories', \
		'http://feeds.abcnews.com/headlinesblog', \
		'http://feeds.abcnews.com/politicsblog', \
		'http://feeds.abcnews.com/businessblog', \
		'http://feeds.abcnews.com/technologyblog', \
		'http://feeds.abcnews.com/lifestyleblog', \
		'http://feeds.abcnews.com/healthblog', \
		'http://www.medicalnewstoday.com/medicalnews.xml', \
		'http://www.medicalnewstoday.com/rss/featurednews.xml', \
		'http://feeds.reuters.com/reuters/businessNews', \
		'http://feeds.reuters.com/reuters/environment', \
		'http://feeds.reuters.com/reuters/healthNews', \
		'http://feeds.reuters.com/reuters/lifestyle', \
		'http://feeds.reuters.com/reuters/MostRead', \
		'http://feeds.reuters.com/reuters/peopleNews', \
		'http://feeds.reuters.com/Reuters/PoliticsNews', \
		'http://feeds.reuters.com/reuters/topNews', \
		'http://feeds.reuters.com/Reuters/domesticNews', \
		'http://feeds.reuters.com/Reuters/worldNews']
N = len(urls)

# Connect to MySQL database "Epidemify"
db = MySQLdb.connect(host='localhost', user='epidemician', \
					passwd='funcrusherplus', db='Epidemify')
cur = db.cursor()
cur.connection.autocommit(True)

# Create an "IE6" browser
br = Browser()
br.set_handle_robots(False)
br.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')]

fields = ['link', 'title', 'summary', 'updated_parsed']
counter = 0
print 'Parsing ' + str(N) + ' RSS feeds...'
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
			if len(e.link) > 65:
				print ' -> ' + e.link[:65] + '...'
			else:
				print ' -> ' + e.link
			html = br.open(e.link).read()
			sqldict['text'] = db.escape_string(nltk.clean_html(html))
		except KeyboardInterrupt:
			quitprompt = raw_input('Quit? [y/N]')
			if quitprompt == 'y' or quitprompt == 'Y':
				raise
			else:
				continue
		except:
			sqldict['text'] = 'NULL'

		# Write RSS and article data to database
		sql = ('INSERT INTO rss_data '
			   '(link, title, summary, updated, article) '
			   'VALUES ('
			   '"%(link)s", "%(title)s", "%(summary)s", "%(updated)s", '
			   '"%(text)s");' % sqldict).replace('"NULL"', 'NULL')
		cur.execute(sql)
	
# Delete duplicate links
print 'Removing duplicate links...'
cur.execute('CREATE TEMPORARY TABLE IF NOT EXISTS rss_temp (id INT UNSIGNED);')
cur.execute('DELETE FROM rss_temp;')
sql = ('INSERT rss_temp (id) '
	   'SELECT id FROM rss_data r WHERE EXISTS ('
	   'SELECT * FROM rss_data r2 '
	   'WHERE r2.link = r.link AND r2.updated > r.updated);')
cur.execute(sql)
cur.execute('DELETE FROM rss_data WHERE id IN (SELECT id FROM rss_temp);')
cur.execute('DROP TABLE rss_temp;')
print str(cur.rowcount) + ' duplicates removed.'

cur.close()
db.close()
