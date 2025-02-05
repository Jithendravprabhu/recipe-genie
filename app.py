from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import psycopg2
import os

app = Flask(__name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if the user is not authenticated

# Fetch the DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)  # Connect using the DATABASE_URL
    return conn

# Define User class to be used with Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Load user from the database (or other storage)
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user_id=user[0])
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for matching username and password
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            login_user(User(user_id=user[0]))  # Log in the user
            return redirect(url_for('home'))  # Redirect to home page if login successful
        else:
            return render_template('login.html', message="Invalid username or password.")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
