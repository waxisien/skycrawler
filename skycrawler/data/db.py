import os
import sqlite3

def dict_factory(cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
      d[col[0]] = row[idx]
  return d


class Sql():

  # SELECT
  get_all_buildings = """
                      SELECT city.name as cname, building.name as bname from building
                      INNER JOIN city ON building.city_id = city.id
                      """

  get_all_cities =  """
                    SELECT id, name from city
                    """

  get_buildings_list_infos =  """
                              SELECT building.name as building_name, city.name as city_name,
                              latitude, longitude, height, floors, link
                              from building INNER JOIN city ON building.city_id = city.id 
                              ORDER BY height DESC LIMIT ?
                              """

  get_cities_with_no_location = """
                                SELECT id, name from city WHERE latitude IS NULL
                                """
  # INSERTS
  create_building = """
                    INSERT INTO building (name, height, floors, link, city_id, status, is_active, creation_date)
                    VALUES(?, ?, ?, ?, ?, ?, 1, datetime())
                    """

  create_city = """
                INSERT INTO city (name, latitude, longitude, creation_date) VALUES(?, ?, ?, datetime())
                """

  # UPDATE
  update_city_latitude =  """
                          UPDATE city SET latitude = ?, longitude = ? WHERE ROWID = ?
                          """

class DataManager():
	
  def __init__(self):
    db_location = os.environ['SKYCRAWLER_DB']
    self._conn = sqlite3.connect(db_location)
    self._conn.row_factory = dict_factory

  def __del__(self):
    self._conn.close()

  def get_buildings(self, limit):

    cursor = self._conn.cursor()
    cursor.execute(Sql.get_buildings_list_infos, (limit, ))
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
