import pytest
from django.contrib.auth.models import User
from django.test import Client
from flashcards.models import Flashcard, Course, Language, List


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def test_user():
    user = User.objects.create_user(
        username="new_user",
        password="new_user"
    )
    return user


@pytest.fixture
def add_courses():
    lang = Language()
    lang.language = "English"
    lang.symbol = "ENG"
    lang.save()

    course = Course()
    course.name = "Test"
    course.language_to_learn = lang
    course.learning_in_language = lang
    course.save()

    new_list = List()
    new_list.name = "Test"
    new_list.learning_in_language = lang
    new_list.language_to_learn = lang
    new_list.courses = course
    new_list.save()

    return new_list


@pytest.fixture
def add_flashcard():
    lang = Language()
    lang.language = "English"
    lang.symbol = "ENG"
    lang.save()

    course = Course()
    course.name = "Test"
    course.language_to_learn = lang
    course.learning_in_language = lang
    course.save()

    new_list = List()
    new_list.name = "Test"
    new_list.learning_in_language = lang
    new_list.language_to_learn = lang
    new_list.courses = course
    new_list.save()

    new_card = Flashcard()
    new_card.front = "Test1"
    new_card.back = "Test2"
    new_card.front_language = lang
    new_card.back_language = lang
    new_card.mastery_level = 2
    new_card.save()
    new_card.lists.add(new_list)

    return new_card
