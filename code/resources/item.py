from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item_model import ItemModel

class Item(Resource): # all resources will be classes which inherit from flask_restful.Resource
  # Add parser to the Item class - - - use: Item.parser
  parser = reqparse.RequestParser()
  parser.add_argument('price', 
    type=float, 
    required=True, 
    help="This field cannot be left blank. Beep boop."
  )
  parser.add_argument('store_id', 
    type=int, 
    required=True, 
    help="Every item needs a store_id."
  )  
  
  @jwt_required()
  def get(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      return item.json(), 200
    return { 'message' : 'Item not found' }, 404
  
  def post(self, name):
    if ItemModel.find_by_name(name):
      return { 'message': 'An item with name {} already exists'.format(name)}, 400
    data = Item.parser.parse_args()
    # item = { 'name': name, 'price': data['price'] }
    item = ItemModel(name, data['price'], data['store_id']) # same as **data
    try:
      item.save_to_db()
    except:
      return { 'message': 'An error occurred inserting the item' }, 500
    return item.json(), 201

  def put(self, name):
    # create item or update an existing one
    data = Item.parser.parse_args() # return only the values from the request body which we specified
    item = ItemModel.find_by_name(name)
    if item is None:
      try:
        item = ItemModel(name, **data) # same as data['price'], data['store_id']
      except:
        return { 'message': 'an error occured inserting the item' }, 500
    else:
      try:
        item.price = data['price']
      except:
        return { 'message': 'an error occured updating the item' }, 500
    item.save_to_db()
    return item.json()

  @jwt_required()
  def delete(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      item.delete_from_db()
    return { 'message': 'Item deleted' }
    # connection = sqlite3.connect('data.db')
    # cursor = connection.cursor()
    # query = "DELETE FROM items WHERE name = ?"
    # cursor.execute(query, (name,))
    # connection.commit()
    # connection.close() 
    # return { 'message': 'Item deleted' }



class ItemList(Resource):
  def get(self):
    # return { 'items': list(map(lambda item: item.json(), ItemModel.query.all())) }
    return { 'items': [item.json() for item in ItemModel.query.all()] }

    