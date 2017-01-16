import os

from flask import Flask, request, Response, jsonify, render_template

from data.db import DataManager

app = Flask(__name__)


@app.route('/raw', methods=['GET'])
def raw():

	db = DataManager()

	data = db.get_buildings(30)

	return render_template('raw.html', buildings=data)


@app.route('/', methods=['GET'])
def map():

	db = DataManager()

	data = db.get_buildings(1000)
	
	return render_template('map.html', 
							buildings=data, 
							MY_GOOGLE_MAP_KEY=os.environ['MY_GOOGLE_MAP_KEY'])


if __name__ == "__main__":
    app.run(debug=True)
