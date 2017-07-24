from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^dashboard', views.dash),
	url(r'^wish_items/create', views.create),
	url(r'^new_item', views.new_item),
	url(r'^wish/(?P<id>\d+)', views.wish),
	url(r'^unwish/(?P<id>\d+)', views.unwish),
	url(r'^delete/(?P<id>\d+)', views.delete),
	url(r'^wish_items/(?P<id>\d+)', views.show)
]