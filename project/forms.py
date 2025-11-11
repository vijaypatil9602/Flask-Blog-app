from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from project.models import User

class RegistrationForm(FlaskForm):
    # 1) Name
    name = StringField('Name', 
                       validators=[DataRequired(), Length(min=2, max=100),
                                   # This is the "alphabets only" rule
                                   Regexp(r'^[A-Za-z ]+$', message="Name must contain only letters and spaces.")])
    
    # --- THIS IS NEW RULE ---
    # 2) Mobile Number
    mobile = StringField('Mobile Number', 
                         validators=[DataRequired(), 
                                     # This regex checks for exactly 10 digits OR exactly 12 digits.
                                     Regexp(r'^(\d{10}|\d{12})$', 
                                            message="Mobile number must be exactly 10 or 12 digits.")])
    # -----------------------------

    # 3) Email ID
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])

    # 4) Address
    address = TextAreaField('Address', 
                            validators=[DataRequired(), 
                                        Length(min=20, max=200, message="Address must be at least 20 characters long.")])

    # 5) Password
    password = PasswordField('Password', 
                             validators=[
                                 DataRequired(), 
                                 Length(min=8),
                                 # Capital letter
                                 Regexp(r'.*[A-Z].*', message="Password must contain at least one capital letter."),
                                 # Number
                                 Regexp(r'.*[0-9].*', message="Password must contain at least one number."),
                                 # Symbol (fixed with \\-)
                                 Regexp(r'.*[!@#$%^&*()_\-+=].*', message="Password must contain at least one symbol (e.g., !@#).")
                             ])

    # 6) Repassword
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    
    submit = SubmitField('Sign Up')

    # Custom validation to check if email is already taken
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

    # Custom validation to check if mobile number is already taken
    def validate_mobile(self, mobile):
        user = User.query.filter_by(mobile=mobile.data).first()
        if user:
            raise ValidationError('That mobile number is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# This is the new form for resetting the password
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])

    password = PasswordField('New Password', 
                             validators=[
                                 DataRequired(), 
                                 Length(min=8),
                                 # We re-use all your strict validation rules here
                                 Regexp(r'.*[A-Z].*', message="Password must contain at least one capital letter."),
                                 Regexp(r'.*[0-9].*', message="Password must contain at least one number."),
                                 Regexp(r'.*[!@#$%^&*()_\-+=].*', message="Password must contain at least one symbol (e.g., !@#).")
                             ])
    
    confirm_password = PasswordField('Confirm New Password', 
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    
    submit = SubmitField('Confirm Password')
    
    # Check if email exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('No account with that email exists.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=20)])
    submit = SubmitField('Post')