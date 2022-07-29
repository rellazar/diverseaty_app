from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.recipes_model import Recipe
from flask_app.models.users_model import User

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id":session['user_id']
    }
    return render_template('new_recipe.html',user=User.get_one_user(data))

@app.route('/create/recipe',methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_sighting(request.form):
        return redirect('/new/sighting')
    data = {
        "name": request.form["name"],
        "ingredients": request.form["ingredients"],
        "descriptions": request.form["descriptions"],
        "country": request.form["country"],
        "user_id": request.form["user_id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:user_id>/<int:recipe_id>')
def edit_recipe(user_id, recipe_id): #user_id
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        "user_id":session['user_id']
    }
    recipe_data = {
        'recipe_id': recipe_id
    }
    return render_template("edit_recipe.html",one_recipe=Recipe.get_one_recipe(recipe_data),user=User.get_one_user(user_data))

@app.route('/update/recipe',methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form["name"],
        "ingredients": request.form["ingredients"],
        "descriptions": request.form["descriptions"],
        "country": request.form["country"],
        "recipe_id": request.form["recipe_id"]
    }
    print(data)
    Recipe.update_recipe(data)
    return redirect('/dashboard')


@app.route('/delete/recipe/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "recipe_id":recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')