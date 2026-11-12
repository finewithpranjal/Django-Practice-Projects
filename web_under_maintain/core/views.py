from django.shortcuts import render

def home(req):
    return render(req, 'core/home.html')

def about(req):
    return render(req, 'core/about.html')

def contact(req):
    return render(req, 'core/contact.html')
