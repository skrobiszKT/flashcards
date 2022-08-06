# Generated by Django 4.0.6 on 2022-07-29 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='back_language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back_lang', to='flashcards.language'),
        ),
        migrations.AlterField(
            model_name='flashcard',
            name='front_language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='front_lang', to='flashcards.language'),
        ),
    ]
