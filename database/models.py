from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 👈 links to User

    user = db.relationship('User', backref='comments') 

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, default=0)

class User(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password_hash = Column(db.Text, nullable=False)  # allows unlimited length


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
def set_password(self, password):
    """
    Set the password for the user by hashing it using werkzeug's generate_password_hash function.

    Parameters:
    password (str): The password to be hashed and set for the user. This parameter should be a string.

    Returns:
    None: This function does not return any value. It sets the hashed password directly to the user's password_hash attribute.
    """
    self.password_hash = generate_password_hash(password)