"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
# 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Halo03117!@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
connect_db(app)

app.config['SECRET_KEY'] = 'cats'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

db.create_all()

#Home page
@app.route('/')
def home():
    return redirect('/users')

#Route for list of users
@app.route('/users')
def list_users():
    all_users = User.query.all()
    return render_template('user_templates/list.html', users = all_users)

#Route for details on specific user
@app.route('/users/details/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_templates/details.html', user = user)


#Route for creating a new user
@app.route('/users/new')
def create_user():
    return render_template('user_templates/new_user.html')

#Route for handling and adding new user to database
@app.route('/users/new/add', methods = ["POST"])
def add_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    image_url = request.form.get("image_url")

    if image_url == '':
       image_url = 'https://p.kindpng.com/picc/s/252-2524695_dummy-profile-image-jpg-hd-png-download.png'

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

# Edit page for a user
@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('user_templates/edit.html', user = user)

# Handles data from edit page, updates db and redirects to that users details
@app.route('/users/<user_id>/edit/update', methods=["POST"])
def update_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get(user_id)
    
    if image_url:
        user.image_url = image_url
    elif image_url == '':
        user.image_url = 'https://p.kindpng.com/picc/s/252-2524695_dummy-profile-image-jpg-hd-png-download.png'

    user.first_name = first_name
    user.last_name = last_name

    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/details/{user_id}')

# Handles deleting of user
@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# Post creation page
@app.route('/users/<user_id>/posts/new')
def new_post(user_id):
    user = User.query.get(user_id)
    tag = Tag.query.all()
    return render_template('post_templates/new_post.html', user = user, tag = tag)

# Handles data from post creation page, updates db and redirects to user details
@app.route('/users/<user_id>/posts/new/update', methods=["POST"])
def create_post(user_id):
    title = request.form["title"]
    content = request.form ["content"]
    tags = request.form.getlist("post_tag")
    user = User.query.get(user_id)

    new_post = Post(title = title, content = content, user_id = user.id)
    db.session.add(new_post)
    db.session.commit()

    
    for tag in tags:
        search_tag = Tag.query.get(tag)
        post_tags = PostTag(post_id = new_post.id, tag_id=search_tag.id)
        db.session.add(post_tags)
        db.session.commit()
        
    return redirect(f'/users/details/{user_id}')
    



# Post details page
@app.route('/posts/<post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_templates/post_details.html', post = post)

# Post edit page
@app.route('/posts/<post_id>/edit', methods = ["GET", "POST"])
def edit_post(post_id):
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = Post.query.get(post_id)

        post.title = title
        post.content = content
        db.session.add(post)
        db.session.commit()
        return redirect(f'/posts/{post_id}')
    else:
        post = Post.query.get(post_id)
        tags = Tag.query.all()
        return render_template('post_templates/edit_post.html', post = post, tags = tags)

# Deletes a post
@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users')



# Shows all tags
@app.route('/tags')
def tag_page():
    tags = Tag.query.all()
    return render_template('tag_templates/tags.html', tags = tags)

# Shows details on a tag
@app.route('/tags/<tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('tag_templates/tag_details.html', tag = tag)

# Adds a tag to the list
@app.route('/tags/new', methods = ["GET", "POST"])
def add_tag_form():
    if request.method == "POST":
        tag_name = request.form["tag_name"]
        new_tag = Tag(name= tag_name)

        db.session.add(new_tag)
        db.session.commit()
        return redirect(f'/tags')

    else:
        return render_template('tag_templates/new_tag.html')

@app.route('/tags/<tag_id>/edit', methods = ["GET", "POST"])
def edit_tag(tag_id):
    if request.method == "POST":
        tag_name = request.form["tag_name"]
        edited_tag = Tag.query.get(tag_id)

        edited_tag.name = tag_name
        db.session.add(edited_tag)
        db.session.commit()
        return redirect(f'/tags')
    else:
        tag = Tag.query.get(tag_id)
        return render_template('tag_templates/edit_tag.html', tag = tag)

@app.route('/tags/<tag_id>/delete', methods = ["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()
    return redirect(f'/tags')
