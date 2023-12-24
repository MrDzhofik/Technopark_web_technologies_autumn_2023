from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from random import randint
from .models import *
from django.views.decorators.http import require_GET
from django.http import Http404
from django.contrib import auth
from .forms import UserForm, AnswerForm, QuestionForm
from django.contrib.auth.models import User

# Create your views here.

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

@login_required
def home(request):
    questions, page, range = paginate(Question.objects.new_rating_order(), request)
    return render(request, 'base/base.html', context={'questions': questions, 'page': page, 'rang': range})

@login_required
def create(request):
    if request.method == "POST":
        if create_question(request):
            return redirect(reverse('home'))
    else:
        form = QuestionForm.QuestionForm()
    context = {'form': form}
    return render(request, 'base/ask.html', context)

def second_page(request):
    return render(request, 'base/second_page.html')

@login_required
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    tags = question.tags.all()
    if request.method == "POST":
        if create_answer(request, question):
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = AnswerForm.AnswerForm()
    answers = Answer.objects.filter(question=question).order_by('-created')
    answers, page, range = paginate(answers, request)
    context = {'question': question, 'answers': answers, 'page': page, 'rang': range, 'tags': tags, 'form': form}
    return render(request, 'base/question.html', context)

def login(request):
    message = ""
    if request.method == "POST":
        form = UserForm.UserForm(request.POST)
        if form.is_valid():
            user = user_auth(request, form)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('home'))
            else:
                message = "Incorrect Login or Password"
    else: 
        form = UserForm.UserForm()
    context = {'form': form, "messages": message}
    return render(request, 'base/login.html', context)

def signup(request):
    message = ''
    if request.method == "POST":
        form = UserForm.UserRegisterForm(request.POST)
        if form.is_valid():
            user = user_reg(request, form)
            if user:
                auth.login(request, user)
                return redirect(reverse('home'))
            else:
                message = "Passwords don't match"
    else:
        form = UserForm.UserRegisterForm()
    context = {'form': form, 'messages': message}
                                
    return render(request, 'base/signup.html', context)

@login_required
def profile(request):
    if request.method == "POST":
        form = UserForm.UserSettingsForm(request.POST)
        if form.is_valid():
            user = user_edit(request, form)
    else:
        form = UserForm.UserSettingsForm()
    context = {'form': form}
    return render(request, 'base/profile.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))

@login_required
@require_GET
def hot(request):
    hot_queryset = Question.objects.hot_rating_order()
    item, page, range = paginate(hot_queryset, request)
    context={'questions': item, 'page': page}
    return render(request, 'base/hot.html', context)

@login_required
@require_GET
def tag(request, tag_name):
    queryset = Question.objects.by_tag(tag_name=tag_name)
    item, page, range = paginate(queryset, request)
    context={'questions': item, 'page': page, 'tag': tag_name}
    return render(request, 'base/tag.html', context)


def user_auth(request, form):
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = auth.authenticate(request, username=username, password=password)
    return user

def user_reg(request, form):
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    confirm_password = form.cleaned_data['confirm_password']
    email = form.cleaned_data['email']
    if password == confirm_password:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user = auth.authenticate(request, username=username, password=password)
        return user
    return False

def user_edit(request, form):
    username = form.cleaned_data['username']
    email = form.cleaned_data['email']
    bio = form.cleaned_data['bio']
    avatar = request.FILES['avatar']
    user = User.objects.get(username=username)
    if email:
        user.email = email
        user.save()
    if avatar:
        try: 
            user_profile = UserProfile.objects.get(user=user)
        except:
            user_profile = UserProfile.objects.create(user=user)
        user_profile.bio = bio
        user_profile.avatar = avatar
        user_profile.save()

    return user

def create_answer(request, question):
    form = AnswerForm.AnswerForm(request.POST)
    if form.is_valid():      
        content = form.cleaned_data['content']
        answer = Answer.objects.create(user=request.user, question=question, content=content)
        answer.save()
        return True
    return False

def create_question(request):
    form = QuestionForm.QuestionForm(request.POST)
    if form.is_valid():      
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        tags = form.cleaned_data['tags']
        question = Question.objects.create(author=request.user, title=title, content=content)
        question.save()
        question.tags.add(*tags)
        return True
    return False