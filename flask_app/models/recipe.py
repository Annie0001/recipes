from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_thirthy_min = data['under_thirthy_min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id= data['user_id']
        self.creator = None
    
    @classmethod
    def get_recipes_from_db(cls):
        query = "SELECT * FROM recipe JOIN users ON recipe.user_id = users.id"

        results = connectToMySQL('recipes_schema').query_db(query)

        print(results)

        recipes = []

        if results:
            for row in results:
                # convert book data from row into object
                recipe = cls(row)
                
                data = {
                    "id" : row['users.id'],
                    "first_name":row['first_name'],
                    "last_name":row['last_name'],
                    "email":row['email'],
                    "password":row['password'],
                    "created_at":row['users.created_at'],
                    "updated_at":row['users.updated_at'],
                }

                recipe.creator = user.User(data)
                print(recipe.creator)
                # add these books into all_books list
                recipes.append(recipe)
        return recipes
    
    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipe where id=%(id)s"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def saved_recipe(cls,data):
        query = "INSERT INTO recipe (name,description,instructions,date_cooked,under_thirthy_min,user_id) VALUES (%(name)s,%(description)s,%(instruction)s,%(date_cooked)s,%(under_thirthy_min)s,%(user_id)s);"
        connectToMySQL('recipes_schema').query_db(query,data)
    
    @classmethod
    def get_recipe_by_user(cls,data):
        query = "SELECT * FROM recipe JOIN users on recipe.user_id = users.id where recipe.id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        print('get_recipe_by_user: ', results)
        row = results[0]
        recipe = cls(row)

        data = {
                    "id" : row['users.id'],
                    "first_name":row['first_name'],
                    "last_name":row['last_name'],
                    "email":row['email'],
                    "password":row['password'],
                    "created_at":row['users.created_at'],
                    "updated_at":row['users.updated_at'],
                }

        recipe.creator = user.User(data)
        return recipe

