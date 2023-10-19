from flask import Flask, render_template, request,redirect,session,flash
from flask_app import app
from flask_app.models.recipe import Recipe


@app.route('/recipes')
def recipes():
    #checking if user is not in session then redirect to /
    if not session.get('fname'):
        return redirect('/')
    
    recipes_from_database = Recipe.get_recipes_from_db()
    return render_template('recipes.html',recipes=recipes_from_database) 

@app.route('/recipes/new')
def create_new_recipe():

    return render_template('new_recipe.html')

@app.route('/recipes/edit/<int:id>')
def show_edit(id):
    data = {
        "id" : id
    }   
    recipe_from_db = Recipe.get_recipe_by_id(data)

    return render_template('show_edit_recipe.html',recipe = recipe_from_db)

@app.route('/recipes/<int:id>', methods=['POST'])
def edit_recipe(id):

    data = {
        "id":id,
        "name":request.form['username'],
        "description":request.form['email'],
        "instructions":request.form['age']

    }   
    # calling model function to save the updated recipe

    return redirect('/recipes')

@app.route('/recipes/new', methods=['POST'])
def new_recipe():
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "date_cooked": request.form['date_cooked'],
        "under_thirthy_min": request.form['under_thirthy_min'],
        "user_id": session['user_id']
        
    }
    Recipe.saved_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>/view')
def view_recipe(id):

    data ={
        # id value comes from the URL
        "id":id
    }
    user_recipe = Recipe.get_recipe_by_user(data)

    return render_template('view_recipe.html', user_recipe = user_recipe)