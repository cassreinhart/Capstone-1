from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name= "index"),
    path('projects/', views.project, name = "project"),
    path('signup', views.signup, name = "signup"),
    path('login', views.login, name = "login"),
]