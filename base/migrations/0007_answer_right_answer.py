# Generated by Django 4.2.6 on 2023-12-27 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_rename_author_answer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='right_answer',
            field=models.BooleanField(default=False),
        ),
    ]