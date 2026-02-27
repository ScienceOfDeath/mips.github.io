from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    public_key = db.Column(db.Text, nullable=True) 
    encrypted_file_path = db.Column(db.String(256), nullable=True)
    encrypted_file_key = db.Column(db.Text, nullable=True) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class EncryptedFile(db.Model):
    __tablename__ = 'encrypted_files'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    
    # db.LargeBinary tells PostgreSQL to use the BYTEA data type for raw bytes
    file_data = db.Column(db.LargeBinary, nullable=False) 
    
    #Keep track of who uploaded it
    uploader_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)