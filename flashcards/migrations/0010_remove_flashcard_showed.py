# Generated by Django 4.0.6 on 2022-08-02 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0009_flashcard_showed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flashcard',
            name='showed',
        ),
    ]
