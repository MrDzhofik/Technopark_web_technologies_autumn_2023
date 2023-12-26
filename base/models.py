from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(default='ronaldo.jpg', upload_to='avatar/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def new_rating_order(self):
        queryset = self.get_queryset()
        return queryset.order_by('-id')

    def hot_rating_order(self):
        queryset = self.get_queryset()
        return queryset.order_by('-likes')


    def by_tag(self, tag_name):
        queryset = self.get_queryset()
        return queryset.filter(tags__name__exact=tag_name)
    
    def by_author(self, author):
        queryset = self.get_queryset()
        return queryset.filter(author__name__exact=author)

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def answers_count(self):
        return self.answers.count()
    
    def likes_count(self):
        return self.likes

    objects = QuestionManager()

    def __str__(self):
        return self.title

class AnswerManager(models.Manager):
    def hot_rating_order(self):
        queryset = self.get_queryset()
        return queryset.order_by('-likes')
    
    def new_rating_order(self):
        queryset = self.get_queryset()
        return queryset.order_by('-created')
        


class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.title}"

class Answer_Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} likes {self.answer}"
    
class Question_LikeManager(models.Manager):
    def toggle_like(self, user, question):
        if self.filter(author=user, question=question).exists():
            self.filter(author=user, question=question).delete()
        else:
            self.create(author=user, question=question)

class Question_Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0)

    objects = Question_LikeManager()

    def __str__(self):
        return f"{self.author.username} likes {self.question}"
