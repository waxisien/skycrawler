import os
import sqlite3

from geopy.geocoders import Nominatim

from utils import sanitizebuilding

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
  return d

class DataManager():
	
  def __init__(self):
    db_location = os.environ['SKYCRAWLER_DB']
    self._conn = sqlite3.connect(db_location)
    self._conn.row_factory = dict_factory

  def __del__(self):
    self._conn.close()

  def get_building_index(self):

    cursor = self._conn.cursor()
    cursor.execute('''SELECT city.name as cname, building.name as bname from building INNER JOIN city ON building.city_id = city.ROWID''')
    buildings = []
    for building in cursor.fetchall():
      buildings.append(sanitizebuilding(building['cname'], building['bname']))

    return buildings

  def get_city_index(self):

    cursor = self._conn.cursor()
    cursor.execute('''SELECT ROWID, name from city''')
    cities = {}
    for city in cursor.fetchall():
      cities[city['name'].lower().replace(' ', '')] = city['rowid']

    return cities

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

  def updatecitycoordonates(self):
    geolocator = Nominatim()
    cursor = self._conn.cursor()

    cursor.execute('''SELECT ROWID, name from city WHERE latitude IS NULL''')
    for city in cursor.fetchall():
      location = geolocator.geocode(city['name'])
      cursor.execute('''UPDATE city SET latitude = ?, longitude = ? WHERE ROWID = ?''',
        (location.latitude, location.longitude, city['rowid']))
      self._conn.commit()

  def get_buildings(self, limit):

    cursor = self._conn.cursor()
    cursor.execute('''SELECT building.name as building_name, city.name as city_name, latitude, longitude, height, floors, link
       from building INNER JOIN city ON building.city_id = city.ROWID ORDER BY height DESC LIMIT ?''', (limit, ))
    data = []
    for url in cursor.fetchall():
      data.append({
            'city': url['city_name'],
            'name': url['building_name'],
            'height':url['height'],
            'link':url['link'],
            'floors': url['floors'],
            'latitude': url['latitude'],
            'longitude': url['longitude']})

    return data

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