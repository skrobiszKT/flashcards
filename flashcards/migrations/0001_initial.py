# Generated by Django 4.0.6 on 2022-07-29 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=64, unique=True)),
                ('symbol', models.CharField(max_length=4, unique=True)),
                ('charset', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flashcard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('front', models.CharField(max_length=64)),
                ('back', models.CharField(max_length=64)),
                ('mastery_level', models.IntegerField(choices=[(1, 'None'), (2, 'Medium'), (3, 'High')], default=1)),
                ('is_difficult', models.BooleanField(default=False)),
                ('tags', models.CharField(max_length=32, null=True)),
                ('back_language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='back_lang', to='flashcards.language')),
                ('front_language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='front_lang', to='flashcards.language')),
            ],
        ),
    ]
