from flask import Blueprint, render_template
from flask_login import login_required, current_user
from project.models import Post # We only need to import Post

# Import the 'dashboard' blueprint
dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard')
@login_required # This is crucial! Only logged-in users can see this.
def user_dashboard():
    # Query the database for posts created *only* by the current user
    posts = Post.query.filter_by(author=current_user)\
                      .order_by(Post.date_posted.desc())\
                      .all()
                      
    # Pass the current user and their posts to the template
    return render_template('dashboard.html', title='My Dashboard', user=current_user, posts=posts)


# --- THIS IS THE /profile ROUTE ---
@dashboard.route('/profile')
@login_required
def profile():
    # current_user is already available, so we just pass it to the template
    return render_template('profile.html', title='My Profile', user=current_user)
    