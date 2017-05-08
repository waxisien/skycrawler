#!/usr/bin/env python

import urllib2
from BeautifulSoup import *
from urlparse import urljoin
import argparse
import re

import context
from skycrawler.data.db import DataManager
from skycrawler.data.utils import sanitizebuilding

class Crawler:

  def __init__(self, db_location, flush_db=False):
    self._buildings = []
    self._cities = {}

    self._db = DataManager()

    if flush_db:
      self._db.deletedb()
    self._db.setupdb()

    # Init url index with previously fetch buildings
    self._buildings = self._db.get_building_index()
    self._cities = self._db.get_city_index()

  # Index an individual page
  def addtoindex(self,url,values):
    city = values[0]
    city_key = values[0].lower().replace(' ', '')
    name = values[1]
    height = None
    floors = None
    latitude = None
    longitude = None
    status = values[-1]
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
      city_id = self._db.insert_city(city, latitude, longitude)
      self._cities[city_key] = city_id
    self._db.insert_building(name, height, floors, url, city_id, status)
    self._buildings.append(sanitizebuilding(city, name))

  def updatecitycoordonates(self):
    self._db.updatecitycoordonates()

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
    return sanitizebuilding(values[0], values[1]) in self._buildings

  def isforumpart(self,url):
    return 'forumdisplay.php' in url or 'showthread.php' in url

  def isfirstpage(self, url):
    return '&page=' not in url

  def isuseful(self, url):
    return url.startswith('http://www.skyscrapercity') and self.isfirstpage(url) and self.isforumpart(url)

  def ismenu(self, url):
    return url.startswith('http://www.skyscrapercity') and 'forumdisplay.php' in url

  # Starting with a list of pages, do a breadth
  # first search to the given depth, indexing pages
  # as we go
  def crawl(self,pages,depth=2):
    for i in range(depth):
      newpages=[]
      for page in pages:
        try:
          headers = { 'User-Agent' : 'Mozilla/5.0' }
          req = urllib2.Request(page, None, headers)
          c=urllib2.urlopen(req)
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

  crawler = Crawler(args.flush_db)

  forums = ['http://www.skyscrapercity.com/forumdisplay.php?f=1720', # Skyscrapers
            'http://www.skyscrapercity.com/forumdisplay.php?f=4070', # Megatalls
            'http://www.skyscrapercity.com/forumdisplay.php?f=1718'] # Proposed skyscrapers

  crawler.crawl(forums, depth=args.depth)

  crawler.updatecitycoordonates()
