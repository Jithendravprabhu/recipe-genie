from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# TheMealDB API Base URL
API_URL = "https://www.themealdb.com/api/json/v1/1/"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')  # Search term (dish name)
    ingredients = request.form.get('ingredients')  # Ingredients input by user
    return get_recipes(query, ingredients)

def get_recipes(query, ingredients):
    # Ensure no empty or invalid search queries
    search_query = f"{query} {ingredients}".strip() if query and ingredients else query or ingredients
    if not search_query:
        return render_template('search_results.html', recipes=[], message="Please provide a dish name or ingredients.")

    try:
        # Call TheMealDB API to search for meals
        url = f'{API_URL}search.php?s={search_query}'
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()

        # Get meals from the API response
        recipes = data.get('meals', [])

        if not recipes:
            return render_template('search_results.html', recipes=[], message="No meals found with your search.")
        
        return render_template('search_results.html', recipes=recipes)
    
    except requests.exceptions.RequestException as e:
        # Handle API request errors (network issues, invalid API, etc.)
        return render_template('search_results.html', recipes=[], message=f"Error: {e}. Please try again later.")

if __name__ == '__main__':
    app.run(debug=True)
