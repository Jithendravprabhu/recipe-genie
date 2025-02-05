from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Fetch the DATABASE_URL from environment variable (set on Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)  # Connect using the DATABASE_URL
    return conn

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
    
    # API integration or database query logic to fetch recipes can go here
    # Example: using an external API for recipe search
    # For now, let's use a mock response for demonstration

    recipes = [{"name": "Pasta", "description": "Delicious pasta with tomato sauce."}]  # Sample data

    return render_template('search_results.html', recipes=recipes)

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
            return redirect(url_for('home'))  # Redirect to home page if login successful
        else:
            return render_template('login.html', message="Invalid username or password.")

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
