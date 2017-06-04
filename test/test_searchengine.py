import os
from mock import patch, Mock

os.environ["SKYCRAWLER_DB"] = ':memory:'

import context
from scripts.searchengine import Crawler
from skycrawler.model import Building


@patch('scripts.searchengine.urllib2.urlopen')
def test_searchengine(urlopen):

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
