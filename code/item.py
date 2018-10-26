from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3

class Item(Resource): # all resources will be classes which inherit from flask_restful.Resource
  # Add parser to the Item class - - - use: Item.parser
  parser = reqparse.RequestParser()
  parser.add_argument('price', 
    type=float, 
    required=True, 
    help="This field cannot be left blank. Beep boop."
  )

  @classmethod
  def find_by_name(cls, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM items WHERE name = ?"
    result = cursor.execute(query, (name,))
    row = result.fetchone()
    connection.close()
    if row:
      return { 'item': { 'name': row[1], 'price': row[2] } }

  @classmethod
  def insert(cls, item):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "INSERT INTO items VALUES (NULL, ?, ?)"
    cursor.execute(query, (item['name'], item['price']))
    connection.commit()
    connection.close() 
  
  @classmethod
  def update(cls, item):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "UPDATE items SET price = ? WHERE name = ?"
    cursor.execute(query, (item['price'], item['name']))
    connection.commit()
    connection.close() 
    
  # @jwt_required()
  def get(self, name):
    item = self.find_by_name(name)
    if item:
      return item, 200
    return { 'message' : 'Item not found' }, 404
  
  def post(self, name):
    if self.find_by_name(name):
      return { 'message': 'An item with name {} already exists'.format(name)}, 400
    data = Item.parser.parse_args()
    item = { 'name': name, 'price': data['price'] }
    try:
      self.insert(item)
    except:
      return { 'message': 'An error occurred inserting the item' }, 500
    return item, 201

  def put(self, name):
    # create item or update an existing one
    data = Item.parser.parse_args() # return only the values from the request body which we specified
    item = self.find_by_name(name)
    updated_item = { 'name': name, 'price': data['price'] }
    if item is None:
      try:
        self.insert(updated_item) # python Dictionary update() method. SHOULD RESEACH BECAUSE DANGEROUS
      except:
        return { 'message': 'an error occured inserting the item' }, 500
    else:
      try:
        self.update(updated_item)
      except:
        return { 'message': 'an error occured updating the item' }, 500
    return updated_item

  # @jwt_required()
  def delete(self, name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "DELETE FROM items WHERE name = ?"
    cursor.execute(query, (name,))
    connection.commit()
    connection.close() 
    return { 'message': 'Item deleted' }


class ItemList(Resource):
  def get(self):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM items"
    result = cursor.execute(query)
    items = []
    for row in result:
      items.append({ 'name': row[0], 'price': row[1] })
    connection.close() 
    if items:
      return { 'items': items }, 200
    return { 'message': 'No items found' }, 404 

    