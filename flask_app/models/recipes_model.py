from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_name = 'diverseaty_schema'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self. ingredients= db_data['ingredients']
        self.descriptions = db_data['descriptions']
        self.country= db_data['country']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.recipe_by= ''
        self.user_id = ''

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_recipes= []
        for row in results:
            print(row['date_of_sighting'])
            recipe = cls(row)
            recipe.user_id = row['user_id']
            recipe.recipe_by = row['first_name'] + row['last_name']
            all_recipes.append(recipe)
        return all_recipes

    @classmethod
    def get_one_recipe(cls,data):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        #one_recipe2 = []
        #for row in results:
            #print(row[''])
        recipe = cls(results[0])
        recipe.reported_by = results[0]['first_name']  #+ results[0]['last_name']
        #one_recipe.append(recipe)
        print (results[0])
        return recipe #one_recipe2

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, ingredients, descriptions, country, user_id) VALUES ( %(name)s,%(ingredients)s,%(description)s,%(country)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, ingredients=%(ingredients)s, descriptions=%(descriptions)s, country=%(country)s, updated_at=NOW() WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        return results

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipess WHERE id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters","recipe")
        if len(recipe['ingredients']) < 2:
            is_valid = False
            flash("Ingredients must be at least 2 characters","recipe")
        if len(recipe['descriptions']) < 1:
            is_valid = False
            flash("Descriptions must be at least 1","sighting")
        if len(recipe['country']) < 2:
            is_valid = False
            flash("Country must be at least 1", "recipe")
        return is_valid