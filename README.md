A cookbook built in `flask` and made static with `Frozen-Flask`. Automatically deployed to `gh-pages` through CircleCI. Recipes are written in a simple YAML markup in the `recipes/` directory following `recipes/template.yaml` and rendered through `jinja2` templates and Bootstrap 5.  

### Running the application

To install, ensure you have the appropriate dependencies and then serve the flask application locally. 

```sh
git clone git@github.com:Chris1221/cookbook.git; cd cookbook
pip install -r requirements.txt
python cookbook/app.py
```

This will serve the application to the default flask port on your localhost (usually 5000). 

### Adding recipes 

Add a new YAML file under `recipes/`. The name, with underscores removed and appropriately capitlized, will be the page extension under `<server>/cookbook/recipe/<recipe_id>.html`.

Follow the `recipes/template.yaml` for all of the available fields. 

```yaml
name: What is it called?
description: What is it
times: How long it takes
quantity: How many does it make?
categories: [tag1, tag2]
ingredients:
  "ingredient": amount
recipe:
  - Recipe steps here
notes:
  - optional
```

### Generating a static website 

To "freeze" the web server and create a listing of static files, I use `Frozen-Flask`:

```sh
python cookbook/freeze.py
```

This will generate a `dist/` folder with all of the appropriate files for static hosting.

### Automating deployment

Deployment is automated with CircleCI. See `.circleci/config.yml`, but in short the CI runs the freeze script to generate a `dist/` folder. I then authenticate back to Github with an SSH personal access token (PAT) and push the `dist/` folder to the `gh-pages` branch of this repository. It is then automatically updated on the web. 
