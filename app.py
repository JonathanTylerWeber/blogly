from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def direct_to_users():
    """redirect to users page"""
    return redirect('/users')  

@app.route('/users')
def list_users():
    """show list of all users"""
    users = User.query.all()
    return render_template('users.html', users=users)  

@app.route('/users/new')
def show_user_form():
    """show form to create new user"""
    return render_template('new.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    """create new user"""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """go to edit page"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user():
    """process update user"""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    updated_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(updated_user)
    db.session.commit()
    return redirect(f'/users/{updated_user.id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
