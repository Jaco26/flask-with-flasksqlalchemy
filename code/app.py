from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
api = Api(app)

#   JWT creates a new endpoint ('/auth')
# When we call /auth, we send a username and password.
# the JWT extension passes that data to the 'authenticate'
# method we imported from our module 'security.py'
# If username and password are legit, /auth returns a JWT which reprensents
# a user's identity
#   We can send that JWT back to a user and when they send further requests
# to other endpoints, JWT uses the 'identity' method imported from 'security.py'
# to get that user's information.
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>') # make the Item resource accessible from the api at the route provided as the second argument
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=5000, debug=True)


