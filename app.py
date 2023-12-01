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
# db.create_all()


@app.route('/')
def list_users()
    """show list of all users"""
    users = User.query.all()
    return render_template('users.html', users=users)  

@app.route('/users/new')
def show_user_form():
    """show form to create new user"""

@app.route('/users/new', methods=['POST'])
def create_user():
    """create new user"""
    first-name = request.form['first-name']
    last-name = request.form['last-name']
    profile-pic = request.form['profile-pic']
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:user_id>')
def show_pet(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)