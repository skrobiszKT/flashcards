# Generated by Django 4.0.6 on 2022-08-08 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0016_remove_list_courses_list_courses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='charset',
        ),
    ]
