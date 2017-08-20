import os
from unittest.mock import patch, Mock

os.environ["SKYCRAWLER_DB"] = ':memory:'

from scripts.searchengine import Crawler
from skycrawler.model import Building, City
from skycrawler.utils import update_city_coordinates


def test_database_begins_empty(db_test):
    assert Building.query.all() == []


@patch('scripts.searchengine.urllib.request.urlopen')
def test_searchengine(urlopen, db_test):

    page_1 = '''
        <body>
            <a href="http://www.skyscrapercity.com/showthread.php?t=1737547">
            CHICAGO | Vista Tower | 362m | 1186ft | 98 fl | U/C
            </a>
            <a href="http://www.skyscrapercity.com/showthread.php?t=7460827">
            NEW YORK | 3WTC (175 Greenwich Street) | 329m | 1079ft | 69 fl | T/O
            </a>
            <a href="http://www.unknownsite.com/showthread.php?t=7460827">
            NEW YORK | 3WTC (175 Greenwich Street) | 329m | 1079ft | 69 fl | T/O
            </a>
            <a href="http://www.skyscrapercity.com/forumdisplay.php?f=902">
            Forum link
            </a>
        </body>
    '''
    page_2 = '''
        <body>
            <a href="http://www.skyscrapercity.com/showthread.php?t=1737547">
            CHICAGO | Vista Tower | 362m | 1186ft | 98 fl | U/C
            </a>
            <a href="http://www.skyscrapercity.com/showthread.php?t=1518868">
            NEW YORK | One Vanderbilt Place | 427m | 1401ft | 58 fl | U/C
            </a>
        </body>
    '''
    a = Mock()
    a.read.side_effect = [page_1, page_2]
    urlopen.return_value = a

    crawler = Crawler(True)

    # Startup page
    forums = ['http://fakepage.com']

    crawler.crawl(forums, depth=2)

    crawled_buildings = Building.query.all()
    assert len(crawled_buildings) == 3

    assert crawled_buildings[0].name == "Vista Tower"
    assert crawled_buildings[0].height == 362
    assert crawled_buildings[0].floors == 98
    assert crawled_buildings[0].city.name == "CHICAGO"


@patch('skycrawler.utils.Nominatim.geocode')
def test_update_city_coordinates(geocode, data_city_no_location):

    class Coordonates:
        latitude = 100
        longitude = 100

    geocode.return_value = Coordonates()

    cities = City.query.all()
    assert len(cities) == 1
    assert cities[0].latitude is None
    update_city_coordinates()

    assert cities[0].latitude == 100
    assert cities[0].longitude == 100
