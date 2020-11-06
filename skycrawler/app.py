from flask import Blueprint,  Flask
from flask_cors import CORS
from flask_graphql import GraphQLView

from skycrawler.schema import schema


main = Blueprint('main', __name__)
cors = CORS()


def create_app():
    app = Flask(__name__)
    cors.init_app(app)
    app.register_blueprint(main)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

    return app
