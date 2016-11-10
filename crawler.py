import urllib2
from BeautifulSoup import *
from urlparse import urljoin
import sqlite3

class crawler:

  def __init__(self):
    self._index = []
    self._conn = sqlite3.connect('skyscrapers.db')

    # Init url index with previously fetch buildings
    cursor = self._conn.cursor()
    cursor.execute('''SELECT link from buildings''')
    for url in cursor.fetchall():
      self._index.append(url[0])

  def __del__(self):
    self._conn.close()

  # Index an individual page
  def addtoindex(self,url,link):
    self._index.append(url);
    values = self.separatewords(link.getText())
    if len(values) > 3:
      cursor = self._conn.cursor()
      cursor.execute('''INSERT INTO buildings VALUES(?, ?, ?, ?, ?, datetime())''', 
        (values[0], values[1], values[2], values[3], url))
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
  def isindexed(self,url):
    return url in self._index

  def isforumpart(self,url):
    return 'forumdisplay.php' in url or 'showthread.php' in url

  def isfirstpage(self, url):
    return '&page=' not in url

  def isuseful(self, url):
    return url[0:4]=='http' and url.startswith('http://www.skyscrapercity') and self.isfirstpage(url) and self.isforumpart(url)

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
            if self.isuseful(url) and not self.isindexed(url):
              self.addtoindex(url, link)
              print self.separatewords(link.getText()), ' ', url
              newpages.append(url)
   	  pages=newpages

      print self._index

  
  # Create the database tables
  def setupdb(self): 
    curs = self._conn.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS buildings
             (city text, name text, height int, floors int, link text, insert_date date)''')
    self._conn.commit()
