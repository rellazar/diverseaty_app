from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models import recipes_model
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db_name = "diverseaty_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one_user(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        user = cls(results[0])
        return user

    @classmethod
    def get_one_user_recipe(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = user_id WHERE users.id = %(user_id)s;"
        #LEFT JOIN recipes ON users.id = user_id
        results = connectToMySQL(cls.db_name).query_db(query,data)
        #user = cls( results[0] )
        #print(results[0])
        # print(results[0]['recipes.id'])
        #for row in results:
        #    if row['recipes.id'] != None:
        #        recipe_data = {
        #            "id": row['recipes.id'],
        #            "name": row['name'],
        #            "ingredients": row['ingredients'],
        #            "descriptions": row['descriptions'],
        #            "country": row['country'],
        #            "created_at": row['recipes.created_at'],
        #            "updated_at": row['recipes.updated_at']
        #        }
        #        recipe = (recipes_model.Recipe(recipe_data))
        #        user.recipes.append(recipe)
        # print (results)
        return cls (results[0])#user
