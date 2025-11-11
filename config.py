import os

# Get the absolute path of the directory where this file is
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Get the secret key from an environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key_for_local_dev'
    
    # --- THIS IS THE IMPORTANT CHANGE ---
    # It looks for the LIVE database URL first.
    # If it can't find it, it uses your local MySQL database for testing.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:root@localhost/my_flask_app'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False 