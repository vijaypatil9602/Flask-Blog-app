from flask import Blueprint, render_template
from project.models import Post # Import the Post model

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Query the database for all posts, ordered by date (newest first)
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts) # Pass posts to the template 