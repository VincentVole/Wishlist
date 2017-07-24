# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def registration_validator(self, postData):
		errors = {}
		#These fields are required.
		#Name and alias fields must consist of only letters.
		if len(postData['name']) < 1:
			errors["name1"] = "Name is required!"
		else:
			if len(postData['name']) < 3:
				errors["name2"] = "Name must be at least 3 characters!"

		if len(postData['username']) < 1:
			errors["username1"] = "Username is required!"
		else:
			if len(postData['username']) < 3:
				errors["username2"] = "Username must be at least 3 characters!"

		if len(postData['password']) < 1:
			errors["password1"] = "Password is required!"
		else:
			#Password can be no fewer than 8 char long.
			if len(postData['password']) < 8:
				errors["password2"] = "Password must be at least 8 characters long!"

		#Password and confirmation field must match.
		if postData['password'] != postData['pass_confirm']:
			errors["password3"] = "Password and confirmation field must match!"

		#Can't make a duplicate account for one username.
		if list(User.objects.filter(username=postData['username'])) != []:
			errors["username3"] = "This username already has an account registered!"

		#Date hired field can't be empty!
		if postData['hired'] == '':
			errors['hired1'] = "Date hired field can't be empty!"
		else:
			#Date hired must be in the past!
			date_format = "%Y-%m-%d"
			input_hired = datetime.strptime(postData['hired'], date_format)
			now = datetime.now()
			if input_hired >= now: #if date hired given is in the future
				errors["hired2"] = "Date hired cannot be in the future!"

		
		return errors;

	def login_validator(self, postData):
		errors = {}
		#Handles case where login fields are empty.
		if len(postData['username']) < 1:
			errors["login"] = "Username and password combination not found in database."
		if len(postData['password']) < 1:
			errors["login"] = "Username and password combination not found in database."
		try:
			user = User.objects.get(username=postData['username'])
			if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				errors["login"] = "Username and password combination not found in database."
		except:
			errors["login"] = "Username and password combination not found in database."
		return errors;

class ItemManager(models.Manager):
	def validator(self,postData):
		errors = {}
		if len(postData['name']) < 1:
			errors["name1"] = "Item field is required!"
		elif len(postData['name']) < 4:
			errors["name2"] = "Item field must be more than 3 characters!"
		return errors


class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	hired = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class Item(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey('User', related_name="items") #user that added the quote
	wish_users = models.ManyToManyField('User', related_name="wish_items")

	objects = ItemManager()