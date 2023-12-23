from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from random import randint
from .models import *
from django.views.decorators.http import require_GET
from django.http import Http404

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
    
    # Вычисляем диапазон страниц
    if number[-1] > 5:
        if page > 4:
            number = range(page - 3, min(paginator.end_index() + 1, page + 4))
        else:
            number = range(1, min(paginator.end_index(), 8))
   

    return paginator.object_list, paginator, number

def home(request):
    questions, page, range = paginate(Question.objects.new_rating_order(), request)
    return render(request, 'base/base.html', context={'questions': questions, 'page': page, 'rang': range})

def create(request):
    return render(request, 'base/ask.html')

def second_page(request):
    return render(request, 'base/second_page.html')

def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question.id)
    tags = question.tags.all()
    answers, page, range = paginate(answers, request)
    context = {'question': question, 'answers': answers, 'page': page, 'rang': range, 'tags': tags}
    return render(request, 'base/question.html', context)

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

@require_GET
def hot(request):
    hot_queryset = Question.objects.hot_rating_order()
    item, page, range = paginate(hot_queryset, request)
    context={'questions': item, 'page': page}
    return render(request, 'base/hot.html', context)

@require_GET
def tag(request, tag_name):
    queryset = Question.objects.by_tag(tag_name=tag_name)
    item, page, range = paginate(queryset, request)
    context={'questions': item, 'page': page, 'tag': tag_name}
    return render(request, 'base/tag.html', context)
