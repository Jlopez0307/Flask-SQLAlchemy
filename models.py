"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def connect_db(app):
    db.app = app

    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id = {u.id} | first_name = {u.first_name} | last_name = {u.last_name} | image_url = {u.image_url}"

    id = db.Column( db.Integer, primary_key=True, autoincrement=True )

    first_name = db.Column( db.String(20))

    last_name = db.Column( db.String(20))

    image_url = db.Column( db.String, server_default = 'https://p.kindpng.com/picc/s/252-2524695_dummy-profile-image-jpg-hd-png-download.png')



class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<post id = {p.id} | title = {p.title} | content = {p.content} | created_at = {p.created_at}"

    id = db.Column( db.Integer, primary_key = True, autoincrement = True)

    title = db.Column( db.String(50) )

    content = db.Column( db.String(50) )

    created_at = db.Column(db.DateTime(timezone=True), server_default = db.func.now() )
    # Has to reference the TABLE when using users.id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Has to reference the CLASS in python when referencing Users
    user = db.relationship('User', backref = 'posts')


class Tag(db.Model):
    """Tags for posts"""

    __tablename__ = "tags"

    id = db.Column( db.Integer, primary_key = True, autoincrement = True )
    name = db.Column( db.String, unique = True, nullable = False)

    assignments = db.relationship('Post', secondary = 'post_tags' , backref = 'tag')


class PostTag(db.Model):
    """Model for accessing both tags and posts"""

    __tablename__ = "post_tags"

    post_id = db.Column( db.Integer, db.ForeignKey('posts.id'), primary_key = True, nullable = False)

    tag_id = db.Column( db.Integer, db.ForeignKey('tags.id'), primary_key = True, nullable = False)

    # __table_args__ = ( db.PrimaryKeyConstraint( post_id , tag_id,),)



