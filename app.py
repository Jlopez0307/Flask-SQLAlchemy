"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
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

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def list_users():
    all_users = Users.query.all()

    return render_template('base.html', users = all_users)

@app.route('/users/new')
def create_user():
    return render_template('new_user.html')


