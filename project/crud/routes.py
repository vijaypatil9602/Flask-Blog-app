from flask import (Blueprint, render_template, redirect, url_for, 
                   flash, request, abort)
from flask_login import current_user, login_required
from project import db
from project.models import Post
from project.forms import PostForm

crud = Blueprint('crud', __name__)


# --- 1. CREATE ---
@crud.route('/post/new', methods=['GET', 'POST'])
@login_required # User must be logged in to create a post
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Create a new Post instance
        post = Post(title=form.title.data, 
                    content=form.content.data, 
                    author=current_user) # 'author' uses the backref
        
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


# --- 2. READ (Single Post) ---
@crud.route('/post/<int:post_id>')
def view_post(post_id):
    # .get_or_404() is a handy way to get an object or return a 404 error
    post = Post.query.get_or_404(post_id) 
    return render_template('post.html', title=post.title, post=post)


# --- 3. UPDATE ---
@crud.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if the current user is the author of the post
    if post.author != current_user:
        abort(403) # 403 Forbidden error
        
    form = PostForm()
    if form.validate_on_submit():
        # Update the post's data
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # No need to add, just commit the changes
        flash('Your post has been updated!', 'success')
        return redirect(url_for('crud.view_post', post_id=post.id))
    elif request.method == 'GET':
        # Pre-populate the form with the current post data
        form.title.data = post.title
        form.content.data = post.content
        
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


# --- 4. DELETE ---
@crud.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))