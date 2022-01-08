from flask import Blueprint, Flask, render_template, request, url_for, session
import json
import os
import yaml
import glob

# Just some convenience methods
def list_recipes():
    return [a.replace("recipes/", "").replace(".yaml", "") for a in glob.glob('recipes/*.yaml') if a != 'recipes/template.yaml']

# Create the blueprint
cookbook = Blueprint('cookbook', __name__, template_folder='templates')

@cookbook.route('/')
def index():
    return render_template('index.html', recipes=list_recipes())

@cookbook.route('/recipe/<recipe_id>.html')
def recipe(recipe_id):
    with open(f"recipes/{recipe_id}.yaml") as f:
        recipe_data = yaml.load(f)
    
    return render_template('recipe.html', recipe=recipe_data)

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