import crawler

crawler = crawler.crawler()
crawler.setupdb()
forums = ['http://www.skyscrapercity.com/forumdisplay.php?f=1720', # Skyscrapers
		  'http://www.skyscrapercity.com/forumdisplay.php?f=4070', # Megatalls
		  'http://www.skyscrapercity.com/forumdisplay.php?f=1718'] # Proposed skyscrapers

crawler.crawl(forums, depth=1)