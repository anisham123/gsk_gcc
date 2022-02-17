# models.py
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import sys
sys.path.append('../..')
from gsk_gcc_dashboard import db


class User(UserMixin, db.Model):
    """User management - Authentication"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}".format(self.name)
