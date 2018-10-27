from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
api = Api(app)

@app.before_first_request
def create_tables():
  db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>') # make the Item resource accessible from the api at the route provided as the second argument
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  # We import the SQLAlchemy instance here because our modules imported above ALSO import it.
  # If we imported it above, we'd be doing a circular import.
  from db import db
  db.init_app(app)
  app.run(port=5000, debug=True)


