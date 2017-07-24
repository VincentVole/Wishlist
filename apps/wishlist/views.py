# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from ..log_and_reg.models import User, Item

# Create your views here.
def dash(request):
	if request.session.get('user_id', False):
		context = {
			'user': User.objects.get(id=request.session['user_id']),
			'items': Item.objects.all(),
			'wishlist': User.objects.get(id=request.session['user_id']).wish_items.all()
		}
		return render(request, 'wishlist/dash.html', context)
	else:
		return redirect('/')

def create(request):
	if request.session.get('user_id', False):
		context = {
			'messages': get_messages(request)
		}
		return render(request, 'wishlist/create.html', context)
	else:
		return redirect('/')

def new_item(request):
	if request.session.get('user_id', False):
		if request.method == "POST":
			errors = Item.objects.validator(request.POST)
			if len(errors):
				for tag, error in errors.iteritems():
					messages.error(request, error, extra_tags=tag)
				return redirect('/wish_items/create')
			else:
				user = User.objects.get(id=request.session['user_id']) #current user
				item = Item.objects.create(name=request.POST['name'], user=user)
				item.wish_users.add(user)
				return redirect('/dashboard')
		else:
			return redirect('/')
	else:
		return redirect('/')

def wish(request, id):
	if request.session.get('user_id', False):
		user = User.objects.get(id=request.session['user_id'])
		item = Item.objects.get(id=id)
		item.wish_users.add(user)
		return redirect('/dashboard')
	else:
		return redirect('/')

def unwish(request, id):
	if request.session.get('user_id', False):
		user = User.objects.get(id=request.session['user_id'])
		item = Item.objects.get(id=id)
		item.wish_users.remove(user)
		return redirect('/dashboard')
	else:
		return redirect('/')

def delete(request, id):
	if request.session.get('user_id', False):
		Item.objects.get(id=id).delete()
		return redirect('/dashboard')
	else:
		return redirect('/')

def show(request, id):
	if request.session.get('user_id', False):
		context = {
			'item': Item.objects.get(id=id),
			'users': Item.objects.get(id=id).wish_users.all()
		}
		return render(request, 'wishlist/wish_item.html', context)
	else:
		return redirect('/')