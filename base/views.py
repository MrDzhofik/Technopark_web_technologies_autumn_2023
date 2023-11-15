from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from random import randint

# Create your views here.

authors = ['Messi', 'Ronaldo', 'MrDzhofik', 'Ramin', 'Nart']
tags = ['Python', 'C++', 'Football', 'World Cup']
QUESTIONS = []
for i in range(30):
    QUESTIONS.append({
        'title': f'title {i}',
        'id': i,
        'text': f'text {i}',
        'tag': tags[randint(0, len(tags) - 1)],
        'author': authors[randint(0, len(authors) - 1)],
        'likes': randint(0, 10)
    })

HOT = QUESTIONS[:8]

def paginate(objects, request, per_page=5):
    page = int(request.GET.get('page', 1))
    paginator = Paginator(objects, per_page)
    number = paginator.page_range
    try: 
        paginator = paginator.page(page)
    except EmptyPage:
        return paginator.page(1).object_list, paginator.page(1), number

    return paginator.object_list, paginator, number

def home(request):
    item, page, range = paginate(QUESTIONS, request)
    return render(request, 'base/base.html', context={'questions': item, 'page': page, 'rang': range})

def create(request):
    return render(request, 'base/ask.html')

def second_page(request):
    return render(request, 'base/second_page.html')

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'base/question.html', {'question': item})

def login(request):
    return render(request, 'base/login.html')

def signup(request):
    return render(request, 'base/signup.html')

def login_err(request):
    return render(request, 'base/login_error.html')

def signup_err(request):
    return render(request, 'base/signup_error.html')

def profile(request):
    return render(request, 'base/profile.html')

def hot(request):
    item, page, range = paginate(HOT, request)
    return render(request, 'base/hot.html', context={'questions': item, 'page': page})

def tag(request, tag_name):
    item = []
    for question in QUESTIONS:
        if question['tag'] == tag_name:
            item.append(question)
    items, page, range = paginate(item, request)
    return render(request, 'base/tag.html', context={'questions': items, 'page': page, 'tag': tag_name})
