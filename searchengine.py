#!/usr/bin/env python

import urllib2
from BeautifulSoup import *
from urlparse import urljoin
import sqlite3
import argparse
import re

from geopy.geocoders import Nominatim

class crawler:

  def __init__(self, flush_db=False):
    self._buildings = []
    self._cities = {}
    self._conn = sqlite3.connect('skyscrapers.db')

    if flush_db:
      self.deletedb()
    self.setupdb()

    # Init url index with previously fetch buildings
    cursor = self._conn.cursor()
    cursor.execute('''SELECT city.name, building.name from building INNER JOIN city ON building.city_id = city.ROWID''')
    for building in cursor.fetchall():
      self._buildings.append(self.sanitizebuilding(building))

    cursor.execute('''SELECT ROWID, name from city''')
    for city in cursor.fetchall():
      self._cities[building[1].lower().replace(' ', '')] = building[0]

  def __del__(self):
    self._conn.close()

  # Create the database tables
  def setupdb(self): 
    curs = self._conn.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS city
              (name text, latitude real, longitude real, creation_date date);''')
    curs.execute('''CREATE TABLE IF NOT EXISTS building
             (name text, height int, floors int, link text, city_id int, creation_date date);''')
    self._conn.commit()

  def deletedb(self):
    curs = self._conn.cursor()
    curs.execute('''DROP TABLE IF EXISTS city''')
    curs.execute('''DROP TABLE IF EXISTS building''')
    self._conn.commit()

  # Index an individual page
  def addtoindex(self,url,values):
    city = values[0]
    city_key = values[0].lower().replace(' ', '')
    name = values[1]
    height = None
    floors = None
    latitude = None
    longitude = None
    for value in values:
      if height is None:
        reg_height_m = re.match(r'~?\+?(?P<height>\d{3,})m', value)
        reg_height_ft = re.match(r'~?\+?(?P<height>\d{3,})ft', value)
        if reg_height_m:
          height = reg_height_m.group('height')
        elif reg_height_ft:
          height = reg_height_ft.group('height')
          height = int(int(height) * 0.3048)

      if floors is None:
        reg_floors = re.match(r'(?P<floors>\d{2,})~?\+? fl', value)
        if reg_floors:
            floors = reg_floors.group('floors')

    if self._cities.get(city_key):
      city_id = self._cities[city_key]
    else:
      city_id = self.insert_city(city, latitude, longitude)
      self._cities[city_key] = city_id
    self.insert_building(name, height, floors, url, city_id)
    self._buildings.append(self.sanitizebuilding(values))

  def insert_building(self, name, height, floors, link, city_id):
    cursor = self._conn.cursor()
    cursor.execute('''INSERT INTO building (name, height, floors, link, city_id, creation_date) VALUES(?, ?, ?, ?, ?, datetime())''',
      (name, height, floors, link, city_id))
    self._conn.commit()

  def insert_city(self, name, latitude, longitude):
    cursor = self._conn.cursor()
    cursor.execute('''INSERT INTO city (name, latitude, longitude, creation_date) VALUES(?, ?, ?, datetime())''',
      (name, latitude, longitude))
    self._conn.commit()
    return cursor.lastrowid

  def getcitycoordonates(self):
    geolocator = Nominatim()
    cursor = self._conn.cursor()

    cursor.execute('''SELECT ROWID, name from city WHERE latitude IS NULL''')
    for city in cursor.fetchall():
      location = geolocator.geocode(city[1])
      cursor.execute('''UPDATE city SET latitude = ?, longitude = ? WHERE ROWID = ?''',
        (location.latitude, location.longitude, city[0]))
      self._conn.commit()

  # Extract the text from an HTML page (no tags)
  def gettextonly(self,soup):
    v=soup.string
    if v==None:   
      c=soup.contents
      resulttext=''
      for t in c:
        subtext=self.gettextonly(t)
        resulttext+=subtext+'\n'
      return resulttext
    else:
      return v.strip()

  # Seperate the words by any non-whitespace character
  def separatewords(self,text):
    return [x.strip() for x in text.split('|')]

  # Return true if this url is already indexed
  def isindexed(self,values):
    return self.sanitizebuilding(values) in self._buildings

  def isforumpart(self,url):
    return 'forumdisplay.php' in url or 'showthread.php' in url

  def isfirstpage(self, url):
    return '&page=' not in url

  def isuseful(self, url):
    return url.startswith('http://www.skyscrapercity') and self.isfirstpage(url) and self.isforumpart(url)

  def ismenu(self, url):
    return url.startswith('http://www.skyscrapercity') and 'forumdisplay.php' in url

  def sanitizebuilding(self, values):
    city = values[0]
    name = values[1]
    return (city+name).lower().replace(' ', '')

  # Starting with a list of pages, do a breadth
  # first search to the given depth, indexing pages
  # as we go
  def crawl(self,pages,depth=2):
    for i in range(depth):
      newpages=[]
      for page in pages:
        try:
          c=urllib2.urlopen(page)
        except:
          print "Could not open %s" % page
          continue
        soup=BeautifulSoup(c.read())
        
      	links=soup('a')
      	for link in links:
          if ('href' in dict(link.attrs)):
            url=urljoin(page,link['href'])
            url=url.split('#')[0]  # remove location portion
            values = self.separatewords(link.getText())
            if len(values) > 3 and self.isuseful(url) and not self.isindexed(values):
              self.addtoindex(url, values)
            # We only parse forum menu pages since they contain thread titles
            if self.ismenu(url) and url not in pages:
              newpages.append(url)
   	  pages=newpages

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Crawler to get latest skyscrapers developpment.')
  
  parser.add_argument('--flush-db', dest='flush_db', action='store_true')
  parser.set_defaults(flush_db=False)
  parser.add_argument("-d", "--depth", type=int, default=1,
                    help="The depth used to crawl the site")

  args = parser.parse_args()

  crawler = crawler(args.flush_db)

  forums = ['http://www.skyscrapercity.com/forumdisplay.php?f=1720', # Skyscrapers
            'http://www.skyscrapercity.com/forumdisplay.php?f=4070', # Megatalls
            'http://www.skyscrapercity.com/forumdisplay.php?f=1718'] # Proposed skyscrapers

  crawler.crawl(forums, depth=args.depth)

  crawler.getcitycoordonates()
