"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users

app = Flask(__name__)
# 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Halo03117!@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

app.config['SECRET_KEY'] = 'cats'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# db.create_all()

#Home page
@app.route('/')
def home():
    return redirect('/users')

#Route for list of users
@app.route('/users')
def list_users():
    all_users = Users.query.all()
    return render_template('list.html', users = all_users)

#Route for details on specific user
@app.route('/users/details/<int:user_id>')
def user_details(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('details.html', user = user)


#Route for creating a new user
@app.route('/users/new')
def create_user():
    return render_template('new_user.html')

#Route for handling and adding new user to database
@app.route('/users/new/add', methods = ["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = Users(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    user = Users.query.get(user_id)
    return render_template('edit.html', user = user)

@app.route('/users/<user_id>/edit/update', methods=["POST"])
def update_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = Users.query.get(user_id)
    
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/details/{user_id}')

@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')




    
