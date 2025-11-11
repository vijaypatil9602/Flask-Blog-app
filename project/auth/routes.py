from flask import Blueprint, render_template, redirect, url_for, flash, request
from project import db, bcrypt
from project.models import User
from project.forms import RegistrationForm, LoginForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create new user
        user = User(name=form.name.data, 
                    email=form.email.data, 
                    mobile=form.mobile.data,
                    address=form.address.data,
                    password=hashed_password)
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists and password is correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Successful!', 'success')
            # Redirect to the page they were trying to access, or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.user_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# It now uses the new ResetPasswordForm
@auth.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # 1. Find user by email
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            # 2. Hash the new password from the form
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            # 3. Update the user's password in the database
            user.password = hashed_password
            db.session.commit()
            
            flash('Your password has been updated! You are now able to log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('No account with that email exists.', 'danger')
            
    return render_template('reset_password.html', title='Reset Password', form=form)