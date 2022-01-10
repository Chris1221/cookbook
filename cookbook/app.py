from flask import Blueprint, Flask, render_template, request, url_for, session
import json
import os
import yaml
import glob

# Just some convenience methods
def list_recipes():
    return [a.replace("recipes/", "").replace(".yaml", "") for a in glob.glob('recipes/*.yaml') if a != 'recipes/template.yaml']

def list_all_in_category(category: str): 
    for r in list_recipes():
        ro = yaml.safe_load(open(f"recipes/{r}.yaml")) 
        if category in ro["categories"]:
            yield r

def list_all_categories():
    recipes = list_recipes()
    categories = []
    for ro in recipes:
        r = yaml.safe_load(open(f"recipes/{ro}.yaml"))
        for category in r["categories"]:
            if category not in categories:
                categories.append(category)

    return categories

# Create the blueprint
cookbook = Blueprint('cookbook', __name__, template_folder='templates')

@cookbook.route('/')
def index():
    return render_template('index.html', recipes=list_recipes())

@cookbook.route('/recipes.html')
def recipe_homepage():
    return render_template('recipes.html', recipes=list_recipes())


@cookbook.route('/category/<category>')
def category(category):
    return render_template('category.html', category=category, recipes=[a for a in list_all_in_category(category)])


@cookbook.route('/recipe/<recipe_id>.html')
def recipe(recipe_id):
    with open(f"recipes/{recipe_id}.yaml") as f:
        recipe_data = yaml.safe_load(f)
    
    return render_template('recipe.html', recipe=recipe_data)

@cookbook.route('/tags.html')


def recipe_tags():
    recipes_in_category = {}
    for category in list_all_categories():
        recipes_in_category[category] = [a for a in list_all_in_category(category)]
    
    return render_template('tags.html', categories=recipes_in_category)


def create_app(test_config=None):
    app = Flask(__name__)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["FREEZER_RELATIVE_URLS"] = True
    app.config["FREEZER_DESTINATION"] = "../dist"
    app.register_blueprint(cookbook)
    return app 

if __name__ == "__main__":
    app = create_app()
    app.run()