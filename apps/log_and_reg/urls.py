from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^main$', views.index),
	url(r'^add$', views.add),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout)
]