from base.models import Tag
from django.contrib.auth.models import User

def top_users_and_tags(request):
    context = {'users': User.objects.all()[:5], 'all_tags': Tag.objects.all()[:5]}
    return context
