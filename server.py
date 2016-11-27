import os
from flask import Flask, request, Response, jsonify, render_template
import sqlite3

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_buildings(limit):
	conn = sqlite3.connect('skyscrapers.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
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

@app.route('/raw', methods=['GET'])
def raw():

    data = get_buildings(30)

    return render_template('raw.html', buildings=data)


@app.route('/', methods=['GET'])
def map():

	data = get_buildings(1000)
	return render_template('map.html', buildings=data)


if __name__ == "__main__":
    app.run(debug=True)
