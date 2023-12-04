"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, DateTime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<User id = {self.id}, first name = {self.first_name}, last name = {self.last_name}, image url = {self.image_url}>"


class Post(db.Model):
    """post model"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    def __repr__(self):
        return f'<Post {self.id}, {self.title}, {self.content}, {self.created_at}, {self.user_id} >'


class Tag(db.Model):
    """tag model"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Tag {self.id}, {self.name} >'


class PostTag(db.Model):
    """relationships between tags and posts"""
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True,)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True,)
