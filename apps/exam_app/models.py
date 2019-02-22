from django.db import models
import re
from datetime import datetime, date
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class BlogManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['email']) < 5:
            errors['email'] = "Invalid email!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords should match!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email!"
        if User.objects.filter(email=postData['email']).count() > 0:
            errors['email'] = "This email already exists!"

        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['email'] = "Invalid email!"
        if User.objects.filter(email=postData['email']).count() < 1:
            errors['email'] = "This email doesnt exist!"
        if len(postData['password']) < 1:
            errors["password"] = "Password should be at least 8 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email!"

        return errors

    def trip_validator(self, postData):
        errors = {}
        print(postData['start_date'])
        if len(postData['destination']) < 3:
            errors['destinations'] = "Destination can't be blank and should be at least 3 characters!"
        if len(postData['plan']) < 3:
            errors['plan'] = "Plan can't be blank and should be at least 3 characters!"
        if len(postData['start_date'])>10:
            errors['start_date'] = "Invalid date format!"
        if len(postData['end_date'])>10:
            errors['start_date'] = "Invalid date format!"
        if postData['start_date']=="":
            errors['start_date'] = "Provide start date!"
        if postData['end_date']=="":
            errors['end_date'] = "Provide end date!"
        if datetime.strptime(postData["start_date"],'%Y-%m-%d') < datetime.now():
            errors["date"] = "Date can't be in past!" 
        if datetime.strptime(postData["end_date"],'%Y-%m-%d') < datetime.now():
            errors["date"] = "Date can't be in past!" 
        if datetime.strptime(postData["end_date"],'%Y-%m-%d')<datetime.strptime(postData["start_date"],'%Y-%m-%d'):
            errors["date"] = "You cant end your trip before you start it!" 

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Trip(models.Model):
    destination = models.CharField(max_length = 45)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField(max_length=255)
    user = models.ForeignKey(User, related_name="trips")
    users = models.ManyToManyField(User, related_name="user_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()
