import os

from flask import Flask, request, Response, jsonify, render_template, Blueprint
from flask_cors import CORS
from flask_graphql import GraphQLView

from skycrawler.model import Building
from skycrawler.schema import schema


main = Blueprint('main', __name__)
cors = CORS()


def create_app():
    app = Flask(__name__)
    cors.init_app(app)
    app.register_blueprint(main)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

    return app


@main.route('/raw', methods=['GET'])
def raw():

    data = Building.query.order_by(Building.height.desc()).filter(Building.is_active == 1).limit(15).all()

    return render_template('raw.html', buildings=data)


@main.route('/', methods=['GET'])
def index():

    buildings = Building.query.order_by(Building.height.desc()).filter(Building.is_active == 1).limit(1000).all()

    data = []
    for building in buildings:
        data.append({'name': building.name,
                     'city': building.city.name,
                     'height': building.height,
                     'latitude': building.city.latitude,
                     'longitude': building.city.longitude,
                     'link': building.link,
                     'status': building.status,
                     })

    return render_template('map.html', buildings=data, MY_GOOGLE_MAP_KEY=os.environ['MY_GOOGLE_MAP_KEY'])
