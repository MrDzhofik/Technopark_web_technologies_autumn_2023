from base.models import Tag
from django.contrib.auth.models import User

def top_users_and_tags(request):
    users = User.objects.all()[:5]
    tags = Tag.objects.all()[:5]
    context = {'users': users, 'all_tags': tags}
    return context
