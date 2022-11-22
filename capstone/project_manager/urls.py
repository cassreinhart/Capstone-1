from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name= "index"),
    path('projects/', views.all_projects, name = "project"),
    path('projects/<int:id>', views.project, name= "detail"),
    path('signup', views.signup, name = "signup"),
    path('login', views.login, name = "login"),
]