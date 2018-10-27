from db import db

class StoreModel(db.Model):
  __tablename__ = 'stores'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))

  # lazy='dynamic' makes self.items a query builder. 
  # if we don't include this argument, when we create the StoreModel
  # sqlalchemy will create a list of objects, one for every item in the items table whose store_id
  # equals a given store's id. EXPENSIVE. lazy='dynamic' lets us specify to only 
  # create the store item objects when we want
  items = db.relationship('ItemModel', lazy='dynamic')

  def __init__(self, name):
    self.name = name

  def json(self):
    return { 
      'name': self.name, 
      'id': self.id, 
      'items': [item.json() for item in self.items.all()] 
    }

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first() # SELECT * FROM __tablename__ WHERE name = name LIMIT 1;

  def save_to_db(self): # this is now an upsert
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
