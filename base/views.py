from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'base/base.html')

def create(request):
    return render(request, 'base/ask.html')

def second_page(request):
    return render(request, 'base/second_page.html')

def question(request):
    return render(request, 'base/question.html')

def login(request):
    return render(request, 'base/login.html')

def signup(request):
    return render(request, 'base/signup.html')

def profile(request):
    return render(request, 'base/profile.html')
