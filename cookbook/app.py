from flask import Blueprint, Flask, render_template, request, url_for, session
import json
import os
import yaml
import glob
from pathlib import Path

from cookbook.parser import MDParser


import git

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

def list_changes(ncommit = 5):
    """List all recent changes in files to generate
    a changelog on the fly.

    Returns:
        List[str]: Messages to display as recipe changes. 
    """

    repo = git.Repo(search_parent_directories=True)
    commits = repo.iter_commits('main', max_count=ncommit)
    
    messages = []
    prev_commit = "HEAD"
    prev_date = ""
    for commit in commits:
        if prev_date == "":
            prev_date = commit.committed_datetime.strftime("%b %d, %Y")
        
        for diff in commit.diff(prev_commit):
            if diff.a_path.startswith("recipes/"):
                name = Path(diff.a_path).stem
                if name != "template":
                    name_nice = " ".join(name.split("_"))

                    change = {}
                    change["date"] = prev_date
                    change["name_nice"] = name_nice
                    change["name"] = name
                    change["new"] = diff.new_file
                    change["type"] = "recipe"
                    messages.append(change)
                    prev_date = commit.committed_datetime.strftime("%b %d, %Y")
                break
            elif diff.a_path.startswith("trips/"):
                name = Path(diff.a_path).stem
                if name != "template":
                    name_nice = " ".join(name.split("_"))

                    change = {}
                    change["date"] = prev_date
                    change["name_nice"] = name_nice
                    change["name"] = name
                    change["new"] = diff.new_file
                    change["type"] = "trip"
                    messages.append(change)
                    prev_date = commit.committed_datetime.strftime("%b %d, %Y")
                break
        prev_commit = commit 
    return messages


# Create the blueprint
cookbook = Blueprint('cookbook', __name__, template_folder='templates')

@cookbook.route('/')
def index():
    return render_template('index.html', recipes=list_recipes(), changes = list_changes(10))

@cookbook.route('/recipes.html')
def recipe_homepage():
    return render_template('recipes.html', recipes=list_recipes())


@cookbook.route('/category/<category>.html')
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


@cookbook.route('/trip/<trip_id>.html')
def trip(trip_id):
    trip = MDParser(f"trips/{trip_id}.md") 
    return render_template('trips/trip.html', trip=trip)

@cookbook.route('/trips.html')
def all_trips():
    trips = []
    for trip in glob.glob('trips/*.md'):
        if trip != 'trips/template.md':
            trips.append(MDParser(trip))

    # Sort by date
    trips.sort(key=lambda x: x.yaml["date"], reverse=True)

    return render_template('trips/all_trips.html', trips=trips)


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