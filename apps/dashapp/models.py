# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        name_regex = re.compile(r'^[A-Z][a-z]+$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pw_regex = re.compile(r'^[a-zA-Z0-9.+_-]{8,}$')

        if len(postData['first_name']) <2:
            errors['first_name'] = 'Name field should have at least 2 characters'
        else:
            if not name_regex.match(postData['first_name']):
                errors['first_name']= 'Incorrect name format'
        ##############        
        if len(postData['last_name']) <2:
            errors['last_name'] = 'Name field should have at least 2 characters'
        else:
            if not name_regex.match(postData['last_name']):
                errors['last_name']= 'Incorrect name format'
        ####################
        if len(postData['email']) <1:
            errors['email'] = 'Email field can not be empty!!!'
        else:
            if not email_regex.match(postData['email']):
                errors['email'] = 'Incorrect email format'
            else:
                if User.objects.filter(email = postData['email']):
                    errors['email'] = 'Email has been registered, Please use other emails.'
        #################
        if len(postData['password']) < 1:
            errors['password']= 'password field can not be empty!!!'
        else:
            if not pw_regex.match(postData['password']):
                errors['password'] = "Password should have at least 8 characters!"
        ################### 
        if len(postData['con_pw']) < 1:
            errors['con_pw']= 'confirm password field can not be empty!!!'
        else:
            if postData['con_pw'] != postData['password']:
               errors['con_pw'] = "Password confirmation do not match!!"  

        return errors

    def login_validator(self, postData):
        errors = {}
        
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pw_regex = re.compile(r'^[a-zA-Z0-9.+_-]{8,}$')

        if len(postData['login_email']) <1 :
            errors['login_email'] = 'Password field can not be empty!!!'
        else:
            if not email_regex.match(postData['login_email']):
                errors['login_email'] = 'Incorrect email format'
            else:
                if not User.objects.filter(email = postData['login_email']):
                    errors['login_email'] = 'Please enter correct email!!'
        #################
        if len(errors) < 1:
            if len(postData['login_pass']) < 1:
                errors['login_pass'] =  'Password field can not be empty!!!'
            else:
                if not pw_regex.match(postData['login_pass']):
                    errors['login_pass'] = "Password should have at least 8 characters!"
                else:
                    user = User.objects.get(email = postData['login_email'])
                    print user.password
                    if not bcrypt.checkpw(postData['login_pass'].encode(), user.password.encode()):
                        errors['login_pass'] = "Incorrect password!"
        return errors

    def update_validator(self, postData):
        errors = {}
        name_regex = re.compile(r'^[A-Z][a-z]+$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) <2:
            errors['first_name'] = 'Name field should have at least 2 characters'
        else:
            if not name_regex.match(postData['first_name']):
                errors['first_name']= 'Incorrect name format'
        ##############        
        if len(postData['last_name']) <2:
            errors['last_name'] = 'Name field should have at least 2 characters'
        else:
            if not name_regex.match(postData['last_name']):
                errors['last_name']= 'Incorrect name format'
        ####################
        if len(postData['email']) <1:
            errors['email'] = 'Email field can not be empty!!!'
        else:
            if not email_regex.match(postData['email']):
                errors['email'] = 'Incorrect email format'
            else:
                other_users = User.objects.exclude(id = postData['id'])
                for user in other_users:
                    if user.email == postData['email']:                
                        errors['email'] = 'Email has been registered, Please use other emails.'
        return errors
    
    def password_validator(self, postData):
        pw_regex = re.compile(r'^[a-zA-Z0-9.+_-]{8,}$')
        errors = {}
        if len(postData['password']) < 1:
            errors['password']= 'password field can not be empty!!!'
        else:
            if not pw_regex.match(postData['password']):
                errors['password'] = "Password should have at least 8 characters!"
        ################### 
        if len(postData['con_pw']) < 1:
            errors['con_pw']= 'confirm password field can not be empty!!!'
        else:
            if postData['con_pw'] != postData['password']:
               errors['con_pw'] = "Password confirmation do not match!!"  

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    desc = models.CharField(max_length=255,default = "")
    user_level = models.IntegerField(default = 1)
    password = models.CharField(max_length=255)
    created_at =  models.DateTimeField(auto_now_add = True)
    
    objects = UserManager()

    def __str__(self):
       return self.first_name + " " + self.last_name

class Message(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(User,related_name = 'post_messages', default = 1)
    receiver = models.ForeignKey(User,related_name = 'messages',default = 1)
    created_at =  models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
    detail = models.TextField()
    message = models.ForeignKey(Message,related_name = 'comments')
    user = models.ForeignKey(User,related_name = 'comments')
    created_at =  models.DateTimeField(auto_now_add = True)