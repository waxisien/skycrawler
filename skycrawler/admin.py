from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from model import Building, City

from database import db_session

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

admin = Admin(app, name='skycrawler', template_mode='bootstrap3')
admin.add_view(ModelView(Building, db_session))
admin.add_view(ModelView(City, db_session))

app.run()

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
