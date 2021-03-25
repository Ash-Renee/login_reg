from django.db import models
import bcrypt
from datetime import datetime
import re
# Create your models here.

class UserManager(models.Manager):
    def validation_login(self, post_data):
        errors = {}

        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            user = user_list[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['password'] = "INVALID CREDENTIALS!"
        else:
            errors['email'] = "INVALID CREDENTIALS!"
        return errors

class UserManager(models.Manager):
    def validation_register(self, post_data):
        # SECONDS_FOR_13_YEARS = 410248800
        DAYS_FOR_13_YEARS = 4749
        errors = {}
    
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be more than 2 letters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be more than 2 letters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        else:
            user_list = User.objects.filter(email= post_data['email'])
            if len(user_list) > 0:
                errors['email'] = "Invalid credentials"

        if len(post_data['birth_date']) < 2:
                errors['birth_date'] = "Must enter birth date"
        else: 
            post_date = datetime.strptime(post_data['birth_date'], "%Y-%m-%d")
            curr_date = datetime.today()
            age = curr_date - post_date 
            if curr_date < post_date:
                errors['birth_date'] = "Birth date must be in the past"
            elif age.days < DAYS_FOR_13_YEARS:
                errors['birth_date'] = "You must be at least 13 years old to register"

        if len(post_data['password']) < 8:
                errors['password'] = "Password must be at least 8 Disney characters long!"
        elif post_data['password'] != post_data['confirm_pw']:
                errors['confirm_pw'] = "Password and Confirm Password must match!"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    birth_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"User {self.first_name} {self.last_name} {self.email}"
