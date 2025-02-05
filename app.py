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
    # Construct search query
    search_query = f"{query} {ingredients}" if query and ingredients else query or ingredients
    if not search_query:
        return render_template('search_results.html', recipes=[], message="Please provide a dish name or ingredients.")

    # Call TheMealDB API to search for meals
    url = f'{API_URL}search.php?s={search_query}'
    response = requests.get(url).json()
    recipes = response.get('meals', [])
    
    if not recipes:
        return render_template('search_results.html', recipes=[], message="No meals found with your search.")
    
    return render_template('search_results.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
