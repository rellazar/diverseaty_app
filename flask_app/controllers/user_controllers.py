from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_reg():
    return render_template('reg.html') #index.html

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'user_id': session['user_id']
    }
    user = User.get_one_user(data)
    all_users = User.get_all()
    return render_template("dashboard.html", user=User.get_one_user(data),recipes=Recipe.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/show_user_page/<int:recipe_id>')
def show_user_page( recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "recipe_id":recipe_id
    }
    user_data = {
        "user_id":session['user_id']
    }
    return render_template("show_recipe.html",one_recipe=Recipe.get_one_recipe(data),user=User.get_one_user_recipe(user_data))