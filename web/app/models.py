from web.app.database import db


class History(db.Document):
    meta = {'collection': 'histories'}

    query = db.StringField()
    created_date = db.DateTimeField()


class Product(db.Document):
    meta = {'collection': 'products'}

    resource = db.StringField()
    history = db.ReferenceField('History')
    url = db.StringField()
    name = db.StringField()
    price = db.FloatField()
    created_date = db.DateTimeField()
