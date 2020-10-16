import certifi
import datetime
import ssl

from geopy.geocoders import Nominatim, options

from skycrawler.database import db_session
from skycrawler.model import Building, City, Synchronization

ctx = ssl.create_default_context(cafile=certifi.where())
options.default_ssl_context = ctx

def sanitize_building(city, name):

    return (city+name).lower().replace(' ', '')


def get_building_index():

    buildings = Building.query.all()
    result = []
    for building in buildings:
        result.append(sanitize_building(building.city.name, building.name))
    return result


def get_city_index():

    cities = City.query.all()
    result = {}
    for city in cities:
        result[city.name.lower().replace(' ', '')] = city.id

    return result


def insert_building(name, height, floors, link, city_id, status):

    city = db_session.query(City).filter(City.id == city_id).first()
    building = Building(name, height, floors, link, city, status, True)
    db_session.add(building)
    db_session.commit()


def insert_city(name, latitude, longitude):

    city = City(name, latitude, longitude)
    db_session.add(city)
    db_session.commit()
    return city.id


def update_city_coordinates():

    geolocator = Nominatim(user_agent='skycrawler-app')

    cities = db_session.query(City).filter(City.latitude == None).all()
    for city in cities:
        location = geolocator.geocode(city.name)
        if location:
            city.latitude = location.latitude
            city.longitude = location.longitude
            db_session.commit()
        else:
            print("Can't find %s coordonates" % city.name)


def insert_synchronization(buildings_retrieved):
    sync = Synchronization(
        syncDate=datetime.datetime.now(),
        buildingsRetrieved=buildings_retrieved,
    )
    db_session.add(sync)
    db_session.commit()