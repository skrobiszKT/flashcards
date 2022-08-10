from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
MASTERY_LEVELS = (
        (1, "Hard"),
        (2, "Good"),
        (3, "Easy"),
        (4, "Excellent")
    )

COURSE_LEVELS = (
    (1, "Beginner"),
    (2, "Elementary"),
    (3, "Intermediate"),
    (4, "Upper Intermediate"),
    (5, "Advanced"),
    (6, "Proficient")
)


class Language(models.Model):
    language = models.CharField(max_length=64, unique=True)
    symbol = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.language


class Course(models.Model):
    name = models.CharField(max_length=64)
    language_to_learn = models.ForeignKey(Language, related_name="front_course_lang", on_delete=models.CASCADE, null=True)
    learning_in_language = models.ForeignKey(Language, related_name="back_course_lang", on_delete=models.CASCADE,
                                             null=True)
    level = models.IntegerField(choices=COURSE_LEVELS, default=1, null=True)
    tags = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=64)
    language_to_learn = models.ForeignKey(Language, related_name="front_list_lang", on_delete=models.CASCADE, null=True)
    learning_in_language = models.ForeignKey(Language, related_name="back_list_lang", on_delete=models.CASCADE,
                                             null=True)
    tags = models.CharField(max_length=32, null=True)
    courses = models.ForeignKey(Course, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    front = models.CharField(max_length=64)
    front_language = models.ForeignKey(Language, related_name="front_lang", on_delete=models.CASCADE, null=True)
    back = models.CharField(max_length=64)
    back_language = models.ForeignKey(Language, related_name="back_lang", on_delete=models.CASCADE, null=True)
    mastery_level = models.IntegerField(choices=MASTERY_LEVELS, default=1)
    is_difficult = models.BooleanField(default=False)
    tags = models.CharField(max_length=32, null=True)
    lists = models.ManyToManyField(List, blank=True)
    image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        self.showed_name = f"{self.front} - {self.back}"
        return self.showed_name


# class FlashcardUser(AbstractUser):
#     courses = models.ManyToManyField(Course, blank=True)
#     lists = models.ManyToManyField(List, blank=True)
#     flashcards = models.ManyToManyField(Flashcard, blank=True)
#     languages_to_learn = models.ManyToManyField(Language, related_name="user_learn_langs", blank=True)
#     learning_in_languages = models.ManyToManyField(Language, related_name="user_langs", blank=True)
