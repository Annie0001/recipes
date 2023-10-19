from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email,password) VALUES(%(fname)s, %(lname)s, %(email)s , %(password)s);"

        return connectToMySQL('recipes_schema').query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        results =  connectToMySQL('recipes_schema').query_db(query,data) 
        # if user with this email does not exist, return false
        if len(results) < 1:
            return False
        
        #create class instance of user returned becasue the user exists with the given email
        user_from_db = cls(results[0])
        return user_from_db

    @staticmethod
    def validate_user(user):
        is_valid = True

        # validation for first name field on registration form
        if len(user["firstname"]) < 2:
            flash('Your Name should have at least 2 characters!!!', 'registration')
            is_valid = False
        if not user["firstname"].isalpha():
            flash('Your Name should contain only letters!!!', 'registration')
            is_valid = False

        # validation for last name field on registration form
        if len(user["lastname"]) < 2:
            is_valid = False
            flash('Your Last Name should have at least 2 characters!!!','registration')
        if not user["lastname"].isalpha():
            flash('Your  Last Name should contain only letters!!!','registration')
            is_valid = False

        #validating email format
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'registration')
            is_valid = False
        
        #validation for email field on registration form
        #checking if email in the registration form exists in the database or not
        data = {
            "email":user["email"]
        }
        # getting user from database by email
        user_in_database = User.get_user_by_email(data)
        
        if user_in_database:
            flash('A user with the given email is already registered. Choose another email.', 'registration')
            is_valid = False

        # Checking the password length
        if len(user['password']) < 8:
            flash('Your password should have at least 8 characters!!!',  'registration')
            is_valid = False

        # confirm password and confrim password fields match
        if user['password'] != user['confPassword']:
            flash('Password and confirm Password do not match! Please enter it again.', 'registration')
            is_valid = False

    
        return is_valid
    
    

