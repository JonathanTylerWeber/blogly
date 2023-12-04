from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

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
    posts = user.posts
    return render_template('user.html', user=user, posts=posts)

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

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def show_post_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def process_post(user_id):
    title = request.form['title']
    content = request.form['content']
    checked_tags = request.form.getlist('tag')
    new_post = Post(title=title, content=content, user_id=user_id)
    for tag_id in checked_tags:
        tag = Tag.query.get(tag_id)
        if tag:
            new_post.tags.append(tag)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show details about a single post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    user = User.query.get_or_404(user_id)
    tags = []
    if post.tags:
        tags = post.tags
    return render_template('post.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """go to edit page for post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    checked_tags = post.tags
    return render_template('edit_post.html', post=post, tags=tags, checked_tags=checked_tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def update_post(post_id):
    """process update post"""
    title = request.form['title']
    content = request.form['content']
    checked_tags = request.form.getlist('tag')
    updated_post = Post.query.get_or_404(post_id)
    updated_post.title = title
    updated_post.content = content
    for tag_id in checked_tags:
        tag = Tag.query.get(tag_id)
        if tag:
            updated_post.tags.append(tag)
    db.session.commit()
    return redirect(f'/posts/{updated_post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """delete post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')

@app.route('/tags')
def show_all_tags():
    """show all tags"""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """show details about one specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html', tag=tag)

@app.route('/tags/new')
def show_tag_form(user_id):
    """Show form to add a tag"""
    return render_template('tag_form.html')

@app.route('/tags/new', methods=['POST'])
def process_tag(tag_id):
    name = request.form['name']
    new_tag = tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """go to edit page for tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    """process update tag"""
    name = request.form['name']
    updated_tag = Tag.query.get_or_404(tag_id)
    updated_tag.name = name
    db.session.commit()
    return redirect(f'/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """delete tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')