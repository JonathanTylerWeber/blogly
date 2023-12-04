from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url='https://ih1.redbubble.net/image.887380338.6324/flat,750x,075,f-pad,750x1000,f8f8f8.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test User</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first-name": "Test", "last-name": "two", "image-url": 'https://ih1.redbubble.net/image.887380338.6324/flat,750x,075,f-pad,750x1000,f8f8f8.jpg'}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Test two</h1>", html)


class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample post."""

        Post.query.delete()

        user = User(first_name="Test", last_name="User", image_url='https://ih1.redbubble.net/image.887380338.6324/flat,750x,075,f-pad,750x1000,f8f8f8.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title='lorem1', content='sadgdfhdsfhsdhfdhdshdfshdf', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        # Delete the post
        Post.query.filter_by(id=self.post_id).delete()

        # Delete the user
        User.query.filter_by(id=self.user_id).delete()

        db.session.commit()

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('lorem1', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>lorem1</h1>', html)

    # def test_add_post(self):
    #     with app.test_client() as client:
    #         d = {"title": "lorem2", "content": "sadgdfhdsfhsdhfdhdshdfshdf", "user_id": "1"}
    #         resp = client.post("/users/1/posts/new", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("lorem2", html)