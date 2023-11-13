from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('ask', views.create, name="create"),
    path('2', views.second_page, name="second_page"),
    path('question', views.question, name="question"),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('login_err', views.login_err, name='login_err'),
    path('signup_err', views.signup_err, name='signup_err'),
]