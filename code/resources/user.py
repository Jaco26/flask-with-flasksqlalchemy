import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel

class UserRegister(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('username', type=str, required=True, help="You must provide a username in order to register")
  parser.add_argument('password', type=str, required=True, help="You must provide a password in order to register")

  def post(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    data = UserRegister.parser.parse_args()
    if UserModel.find_by_username(data['username']):
      return { 'message': 'User with username: "{}" already exists in database'.format(data['username'])}, 400
    query = "INSERT INTO users VALUES (NULL, ?, ?)" # id column is auto incrementing so we must insert NULL as a placeholder in VALUES
    cursor.execute(query, (data['username'], data['password']))
    connection.commit()
    connection.close()

    return { 'message': 'User created successfully.' }, 201