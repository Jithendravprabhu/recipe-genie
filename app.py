from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

SPOONACULAR_API_KEY = 'c5536c5232b34c3fbdcc8f8524b347c4'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    return redirect(url_for('results', query=query))

@app.route('/results/<query>')
def results(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={SPOONACULAR_API_KEY}'
    response = requests.get(url).json()
    results = response.get('results', [])
    return render_template('search_results.html', query=query, results=results)

@app.route('/recipe/<int:recipe_id>')
def recipe_details(recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOONACULAR_API_KEY}'
    recipe = requests.get(url).json()
    return render_template('recipe_details.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
