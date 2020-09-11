import os
from unittest.mock import patch, Mock

os.environ["SKYCRAWLER_DB"] = ':memory:'

from scripts.searchengine import Crawler
from skycrawler.model import Building, City
from skycrawler.utils import update_city_coordinates


def test_database_begins_empty(db_test):
    assert Building.query.all() == []


@patch('scripts.searchengine.urlopen')
def test_searchengine(urlopen, db_test):

    page_1 = '''
        <body>
            <a href="/threads/jakarta-thamrin-nine-towers-383m-1256ft-75-fl-275m-902ft-62-fl-u-c.1646674/">
            JAKARTA | Thamrin Nine Towers | 383m | 1256ft | 75 fl | 275m | 902ft | 62 fl | U/C
            </a>
            <a href="/threads/kuala-lumpur-tower-m-klcc-700m-2296ft-145-fl-prep.1639309/">
            KUALA LUMPUR | Tower M KLCC | 700m+ | 2296ft+ | 145 fl | Prep
            </a>
            <a href="/threads/seoul-yongsan-international-business-district-621m-2037ft-pro.2000974/">
            SEOUL | Yongsan International Business District | 621m | 2037ft | Pro
            </a>
            <a href="/forums/megatalls.4070/watch">
            Forum link
            </a>
        </body>
    '''
    page_2 = '''
        <body>
            <a href="/threads/seoul-yongsan-international-business-district-621m-2037ft-pro.2000974/">
            SEOUL | Yongsan International Business District | 621m | 2037ft | Pro
            </a>
            <a href="/threads/moscow-neva-towers-345m-1132ft-79-fl-302m-991ft-69-fl-t-o.396624/">
            MOSCOW | NEVA Towers | 345m | 1132ft | 79 fl | 302m | 991ft | 69 fl | T/O
            </a>
        </body>
    '''
    a = Mock()
    a.read.side_effect = [page_1, page_2]
    urlopen.return_value = a

    crawler = Crawler(True)

    # Startup page
    forums = ['https://www.skyscrapercity.com/fakepage']

    crawler.crawl(forums, depth=2)

    crawled_buildings = Building.query.all()
    assert len(crawled_buildings) == 4

    assert crawled_buildings[0].name == "Thamrin Nine Towers"
    assert crawled_buildings[0].height == 383
    assert crawled_buildings[0].floors == 75
    assert crawled_buildings[0].city.name == "JAKARTA"


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
