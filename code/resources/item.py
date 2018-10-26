from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item_model import ItemModel
import sqlite3

class Item(Resource): # all resources will be classes which inherit from flask_restful.Resource
  # Add parser to the Item class - - - use: Item.parser
  parser = reqparse.RequestParser()
  parser.add_argument('price', 
    type=float, 
    required=True, 
    help="This field cannot be left blank. Beep boop."
  )
    
  # @jwt_required()
  def get(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      print('item.json', item.json())
      return item.json(), 200
    return { 'message' : 'Item not found' }, 404
  
  def post(self, name):
    if ItemModel.find_by_name(name):
      return { 'message': 'An item with name {} already exists'.format(name)}, 400
    data = Item.parser.parse_args()
    # item = { 'name': name, 'price': data['price'] }
    item = ItemModel(name, data['price'])
    try:
      item.insert()
    except:
      return { 'message': 'An error occurred inserting the item' }, 500
    return item.json(), 201

  def put(self, name):
    # create item or update an existing one
    data = Item.parser.parse_args() # return only the values from the request body which we specified
    item = ItemModel.find_by_name(name)
    updated_item = ItemModel(name, data['price'])
    if item is None:
      try:
        updated_item.insert() # python Dictionary update() method. SHOULD RESEACH BECAUSE DANGEROUS
      except:
        return { 'message': 'an error occured inserting the item' }, 500
    else:
      try:
        updated_item.update()
      except:
        return { 'message': 'an error occured updating the item' }, 500
    return updated_item.json()

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
      items.append({ 'name': row[1], 'price': row[2] })
    connection.close() 
    if items:
      return { 'items': items }, 200
    return { 'message': 'No items found' }, 404 

    