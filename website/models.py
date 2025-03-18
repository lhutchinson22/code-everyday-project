from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    def set_password(self, password):
        """Set the user's password hash"""
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password, password)
