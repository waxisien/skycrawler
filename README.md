# skycrawler

A crawler and a webpage to display latest worldwide highrises developments. Data fetched from [skyscrapercity.com](http://www.skyscrapercity.com) forum.

![drawing](example.png)

## How to use

Setup the virtualenv:
```
mkvirtualenv -p `which python2.7` skyscraper
pip install -r skycrawler.req
```

Install front-end dependencies:
```
npm install
bower install
```

Indicates where to find your sqlite database:
```
export SKYCRAWLER_DB=your_db_path
```

Get data:
```
./scripts/searchengine.py
```

Compile javascript, launch flask and browse page:
```
gulp
python skyscrawler/app.py
```

Admin access:
```
python skycrawler/admin.py
```
