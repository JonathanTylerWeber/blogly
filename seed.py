from models import Post, User, db, Tag
from app import app
from sqlalchemy import Column, DateTime

db.drop_all()
db.create_all()

u1 = User(first_name='Jonathan', last_name='Weber', image_url='https://i.pinimg.com/736x/ab/c4/8b/abc48b4afe75a9c72f5cc162e6bf2be9.jpg')
u2 = User(first_name='Abigail', last_name='Li', image_url='https://i.pinimg.com/736x/ab/c4/8b/abc48b4afe75a9c72f5cc162e6bf2be9.jpg')
u3 = User(first_name='Kali', last_name='Weber', image_url='https://i.pinimg.com/736x/ab/c4/8b/abc48b4afe75a9c72f5cc162e6bf2be9.jpg')

p1 = Post(title='lorem1', content='sadgdfhdsfhsdhfdhdshdfshdf', user_id='1')
p2 = Post(title='lorem2', content='sadgdfhdsfhsdhfdhdshdfshdf', user_id='1')
p3 = Post(title='lorem3', content='sadgdfhdsfhsdhfdhdshdfshdf', user_id='2')
p4 = Post(title='lorem4', content='sadgdfhdsfhsdhfdhdshdfshdf', user_id='2')
p5 = Post(title='lorem5', content='sadgdfhdsfhsdhfdhdshdfshdf', user_id='3')

t1 = Tag(name='hot')
t2 = Tag(name='cool')
t3 = Tag(name='awesome')

users = [u1, u2, u3]
db.session.add_all(users)
db.session.commit()

posts = [p1, p2, p3, p4, p5]
db.session.add_all(posts)
db.session.commit()

tags = [t1, t2, t3]
db.session.add_all(tags)
db.session.commit()