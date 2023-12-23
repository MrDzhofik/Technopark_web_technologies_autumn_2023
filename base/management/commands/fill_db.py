from django.core.management.base import BaseCommand
from base.models import *
from faker import Faker
import random

class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    # handle argument from command prompt 
    def handle(self, *args, **options):
        ratio = options['ratio']

        users_count = ratio
        questions_count = ratio * 10
        answers_count = ratio * 100
        tags_count = ratio
        question_likes_count = ratio * 100
        answer_likes_count = ratio * 100
        
        # self.create_fake_users(users_count)
        # self.create_fake_questions(questions_count)
        # self.create_fake_answers(answers_count)
        # self.create_fake_tags(tags_count)
        # self.put_tags_to_questions()
        # self.like_questions(question_likes_count)
        # self.like_answers(answer_likes_count)
        # self.create_likes_values()
        self.create_likes_to_questions()

        self.create_likes_to_answers()

    def create_fake_users(self, count):
        print('Create users')
        words = list(set(self.fake.words(nb=100000)))
        random.shuffle(words)
        usernames = []
        i = 0
        while i < count:
            for first_word in words:
                for second_word in words:
                    usernames.append(first_word + second_word)
                    i += 1
        users = [User(username=usernames[i],
                    email = self.fake.email(),
                    password = self.fake.password())
                for i in range(count)]

        User.objects.bulk_create(users)
        print('Finish users')

    def create_fake_questions(self, count):
        users = User.objects.all()

        print('Create questions')
        questions = [Question(title=self.fake.sentence(),
                              content=self.fake.text(),
                              author=random.choice(users))
                     for _ in range(count)]

        Question.objects.bulk_create(questions)

        print('Finish questions')


    def create_fake_answers(self, count):
        users = User.objects.all()
        questions = Question.objects.all()
        print('Start answers')

        answers = [Answer(question=random.choice(questions),
                          content=self.fake.text(),
                          user=random.choice(users))
                    for _ in range(count)]

        Answer.objects.bulk_create(answers)

        print('Finish answers')


    def create_fake_tags(self, count):

        print('Start tags')

        words = list(set(self.fake.words(nb=10000)))
        random.shuffle(words)
        tag_names = []
        i = 0
        while i < count:
            for first_word in words:
                for second_word in words:
                    tag_names.append(first_word + second_word)
                    i += 1
        tags = [Tag(name=tag_names[i]) for i in range(count)]

        Tag.objects.bulk_create(tags)
        print('Finish tags')


    def like_questions(self, count):
        users = User.objects.all()
        questions = Question.objects.all()

        print ('Start liking questions')

        questionlikes = [Question_Like(question=random.choice(questions),
                                      author=random.choice(users))
                         for _ in range(count)]

        Question_Like.objects.bulk_create(questionlikes)

        print('Finish liking questions')


    def like_answers(self, count):
        users = User.objects.all()
        answers = Answer.objects.all()

        print ('Start liking answers')

        answerlikes = [Answer_Like(answer=random.choice(answers),
                                    user=random.choice(users))
                      for _ in range(count)]

        Answer_Like.objects.bulk_create(answerlikes)

        print('Finish liking answers')

    def put_tags_to_questions(self):
        tags = Tag.objects.all()

        print('Start putting tags on questions')
        for question in Question.objects.all():
            tags_to_add = random.choices(tags, k=2)
            for tag in tags_to_add:
                question.tags.add(tag.id)
                question.save()

        print('Finish putting tags on questions')

    def create_likes_values(self):
        questionlikes = Question_Like.objects.all()
        val_list = [-1, 0, 1]

        print('Start putting values to questionlikes')
        for questionlike in questionlikes:
            val = random.choice(val_list)
            questionlike.value = val
            questionlike.save()

        print('Finished putting values')

        answerlikes = Answer_Like.objects.all()
        print('Start putting value to answerlikes')
        for answerlike in answerlikes:
            val = random.choice(val_list)
            answerlike.value = val
            answerlike.save()
        print('Finished putting answerlike values')


    def create_likes_to_questions(self):

        questions = Question.objects.all()
        print('Start counting question likes')

        for question in questions:
            for like in question.question_like_set.all():
                question.likes = question.likes + like.value
                question.save()


        print('Finished counting question likes')


    def create_likes_to_answers(self):
        answers = Answer.objects.all()
        print('Start counting answer likes')

        for answer in answers:
            for like in answer.answer_like_set.all():
                answer.likes = answer.likes + like.value
                answer.save()


        print('Finished counting answer likes')

