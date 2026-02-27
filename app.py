import hashlib
import time
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
app.secret_key = 'insanely-super-secret-key'


#config database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_q7gRM2AFdLlJ@ep-crimson-glitter-ag5fi36n-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init database
db = SQLAlchemy(app)

# 4. Define the User Table
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

#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find the user by their username
        user = User.query.filter_by(username=username).first()
        
        # If the user exists AND the password matches the hash
        if user and user.check_password(password):
            return f"Welcome back, {username}! You are logged in."
        else:
            return "Error: Invalid username or password."

    # Show the login form
    return render_template('login.html', msg = msg)

#Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    # If the user clicks "Submit" on the form, it sends a POST request
    if request.method == 'POST':
        # Grab the data from the form
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            return "Error: User already exists! Try another username."
            
        # Create the new user and save to database
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return f"Success! User '{username}' has been registered."
        
    # If it's a GET request, just show them the blank HTML form
    return render_template('register.html', msg = msg)


@app.route('/')

def flask_app():

    password = b'Humm3rsupp3!'

    password_hash = hashlib.sha256(password)

    print(password_hash)

    return 'Done'


if __name__ == '__main__':
    app.run()

# test