#!/usr/bin/env python

import re
import argparse
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from urllib.error import URLError

from bs4 import BeautifulSoup
from progress.spinner import Spinner

from skycrawler import database
from skycrawler import utils


class Crawler:

    def __init__(self, init_db=False):

        if init_db:
            database.drop_db()
            database.init_db()

        # Init url index with previously fetch buildings
        self._buildings = utils.get_building_index()
        self._cities = utils.get_city_index()

    # Index an individual page
    def add_to_index(self, url, values):
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
            city_id = utils.insert_city(city, latitude, longitude)
            self._cities[city_key] = city_id
        utils.insert_building(name, height, floors, url, city_id, status)
        self._buildings.append(utils.sanitize_building(city, name))

    @staticmethod
    def update_city_coordonates():
        utils.update_city_coordinates()

    # Extract the text from an HTML page (no tags)
    def get_text_only(self, soup):
        v = soup.string
        if v is None:
            c = soup.contents
            result_text = ''
            for t in c:
                subtext = self.get_text_only(t)
                result_text += subtext+'\n'
            return result_text
        else:
            return v.strip()

    # Separate the words by any non-whitespace character
    @staticmethod
    def split_words(text):
        return [x.strip() for x in text.split('|')]

    # Return true if this url is already indexed
    def is_indexed(self, values):
        return utils.sanitize_building(values[0], values[1]) in self._buildings

    @staticmethod
    def is_forum_part(url):
        return 'forumdisplay.php' in url or 'showthread.php' in url

    @staticmethod
    def is_first_page(url):
        return '&page=' not in url

    @staticmethod
    def is_useful(url):
        return url.startswith('http://www.skyscrapercity') and Crawler.is_first_page(url) and Crawler.is_forum_part(url)

    @staticmethod
    def is_menu(url):
        return url.startswith('http://www.skyscrapercity') and 'forumdisplay.php' in url

    # Starting with a list of pages, do a breadth
    # first search to the given depth, indexing pages
    # as we go
    def crawl(self, pages, depth=1):
        spinner = Spinner('Searching ')
        for i in range(depth):
            newpages = []
            for page in pages:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    req = Request(page, None, headers)
                    c = urlopen(req)
                except URLError:
                    print("Could not open %s" % page)
                    continue
                soup = BeautifulSoup(c.read(), "html.parser")

                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        url = url.split('#')[0]  # remove location portion
                        values = self.split_words(link.getText())
                        if len(values) > 3 and self.is_useful(url) and not self.is_indexed(values):
                            self.add_to_index(url, values)
                        # We only parse forum menu pages since they contain thread titles
                        if self.is_menu(url) and url not in pages:
                            newpages.append(url)
                        spinner.next()
            # Update pages to crawl
            pages = newpages

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Crawler to get latest skyscrapers developpment.')

    parser.add_argument('--init-db', dest='init_db', action='store_true',
                        help="Init database, drop if already exist")
    parser.set_defaults(init_db=False)
    parser.add_argument("-d", "--depth", type=int, default=1,
                        help="The depth used to crawl the site")

    args = parser.parse_args()

    crawler = Crawler(args.init_db)

    forums = ['http://www.skyscrapercity.com/forumdisplay.php?f=1720',  # Skyscrapers
              'http://www.skyscrapercity.com/forumdisplay.php?f=4070',  # Megatalls
              'http://www.skyscrapercity.com/forumdisplay.php?f=1718']  # Proposed skyscrapers

    crawler.crawl(forums, depth=args.depth)

    crawler.update_city_coordonates()
