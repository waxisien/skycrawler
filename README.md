# skycrawler

[![Build Status](https://travis-ci.org/waxisien/skycrawler.svg?branch=master)](https://travis-ci.org/waxisien/skycrawler)
[![Coverage Status](https://coveralls.io/repos/github/waxisien/skycrawler/badge.svg)](https://coveralls.io/github/waxisien/skycrawler)

A crawler and a webpage to display latest worldwide highrises developments. Data fetched from [skyscrapercity.com](http://www.skyscrapercity.com) forum.

![drawing](example.png)

## How to use

Setup the virtualenv:
```
mkvirtualenv -p `which python3.5` skyscraper
pip install -r skycrawler.req
pip install -e .
```

Install front-end dependencies:
```
npm install
bower install
```

Set a few env variables:
```
export SKYCRAWLER_DB=<your sql lite db path>
export MY_GOOGLE_MAP_KEY=<google map key>
```

Get data:
```
./scripts/searchengine.py --init-db
```

Compile javascript, launch flask and browse page:
```
gulp
python skyscrawler/app.py
```

Admin access:
```
export SKY_ADMIN_SETTINGS=../conf/admin.cfg
python skycrawler/admin.py
```

Unit test:
```
pip install pytest
pytest .
```
