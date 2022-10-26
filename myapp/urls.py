from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('editprofile', views.edit),
    path('getcity', views.getcity),
    path('upload', views.upload),
    path('process_edit', views.process_edit),
    path('logout', views.logout),
]