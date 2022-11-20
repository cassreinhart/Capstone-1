from django.shortcuts import render

def welcome(response):
    return render(response, 'project/index.html')
