# Generated by Django 4.0.6 on 2022-08-09 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0021_alter_flashcarduser_options_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FlashcardUser',
        ),
    ]
