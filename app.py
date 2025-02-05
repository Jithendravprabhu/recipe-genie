from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import bcrypt

app = Flask(__name__)

# Fetch the DATABASE_URL from environment variable (set on Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to get a database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)  # Connect using the DATABASE_URL
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')  # Search term (dish name)
    ingredients = request.form.get('ingredients')  # Ingredients input by user
    return get_recipes(query, ingredients)

def get_recipes(query, ingredients):
    search_query = f"{query} {ingredients}".strip() if query and ingredients else query or ingredients
    if not search_query:
        return render_template('search_results.html', recipes=[], message="Please provide a dish name or ingredients.")
    
    # Get recipes from the database based on user input
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes WHERE name LIKE %s OR ingredients LIKE %s", (f"%{search_query}%", f"%{search_query}%"))
        recipes = cursor.fetchall()
        conn.close()

        if not recipes:
            return render_template('search_results.html', recipes=[], message="No meals found.")
        return render_template('search_results.html', recipes=recipes)
    else:
        return render_template('search_results.html', recipes=[], message="Error: Could not connect to the database.")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the database for matching username and password
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            conn.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):  # user[1] should be the hashed password
                return redirect(url_for('home'))  # Redirect to home page if login successful
            else:
                return render_template('login.html', message="Invalid username or password.")
        else:
            return render_template('login.html', message="Error: Could not connect to the database.")

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
