from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('ask', views.create, name="create"),
    path('2', views.second_page, name="second_page"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('hot', views.hot, name='hot'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('profile/edit', views.profile, name='profile'),
    path('logout', views.logout, name='logout')
]