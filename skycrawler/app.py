import os

from flask import Flask, request, Response, jsonify, render_template

from model import Building

app = Flask(__name__)


@app.route('/raw', methods=['GET'])
def raw():

    data = Building.query.order_by(Building.height.desc()).limit(15).all()

    return render_template('raw.html', buildings=data)


@app.route('/', methods=['GET'])
def map():

    buildings = Building.query.order_by(Building.height.desc()).limit(1000).all()

    data = []
    for building in buildings:
        data.append({'name': building.name,
                     'city': building.city.name,
                     'height': building.height,
                     'latitude': building.city.latitude,
                     'longitude': building.city.longitude,
                     'link': building.link})

    return render_template('map.html', buildings=data, MY_GOOGLE_MAP_KEY=os.environ['MY_GOOGLE_MAP_KEY'])


if __name__ == "__main__":
    app.run(debug=True)
