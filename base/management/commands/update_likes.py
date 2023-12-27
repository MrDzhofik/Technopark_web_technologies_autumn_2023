from django.core.management.base import BaseCommand
from base.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.update_likes()
    
    def update_likes(self):
        questions = Question.objects.all()
        for question in questions:
            id = question.id
            likes_count = Question_Like.objects.filter(question=question)
            value = 0
            for like in likes_count:
                value += like.value
            Question.objects.filter(pk=id).update(likes=value)