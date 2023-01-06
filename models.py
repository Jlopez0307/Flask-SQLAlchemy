"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    db.app = app

    db.init_app(app)

class Users(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id = {u.id} | first_name = {u.first_name} | last_name = {u.last_name} | image_url = {u.image_url}"

    id = db.Column( db.Integer, primary_key=True, autoincrement=True )

    first_name = db.Column( db.String(20))

    last_name = db.Column( db.String(20))

    image_url = db.Column( db.String(100), default = 'https://www.shutterstock.com/image-vector/empty-photo-male-profile-gray-260nw-538707310.jpg')

