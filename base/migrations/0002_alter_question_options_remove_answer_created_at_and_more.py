# Generated by Django 4.2.6 on 2023-12-23 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={},
        ),
        migrations.RemoveField(
            model_name='answer',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='question',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='question',
            name='updated',
        ),
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answer_like',
            name='value',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question_like',
            name='value',
            field=models.SmallIntegerField(default=0),
        ),
    ]
