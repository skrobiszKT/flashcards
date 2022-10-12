import pytest
from django.contrib.auth.models import User
from tests.conftest import client, test_user
from flashcards.models import List, Course, Flashcard


@pytest.mark.django_db
def test_login(client, test_user):
    response = client.post("/login/", {"username": "new_user", "password": "wrongpass"})

    assert response.url == "/login/"

    response = client.post("/login/", {"username": "new_user", "password": "new_user"})

    assert response.url == "/"


@pytest.mark.parametrize("url", ["/add_multiple_flashcards/", '/show_all/courses/add/', '/add_language/', '/add_list/',
                                 '/edit_languages/'])
@pytest.mark.django_db
def test_login_access(client, test_user, url):
    client.login(username="new_user", password="new_user")
    response = client.get(url)

    assert response.status_code == 200

    client.logout()
    response = client.get(url)

    assert response.status_code != 200


@pytest.mark.django_db
def test_add_multiple(client, test_user, add_courses):
    test_login(client, test_user)
    assert Course.objects.all().count() > 0

    response = client.post("/add_multiple_flashcards/",
                           {'list': ['1'], 'front_lang': ['1'], 'back_lang': ['1'], 'cards': ['Card1; Cards2']})

    assert response.url == "/show_all/flashcards/"

    assert Flashcard.objects.filter(front="Card1").count() == 1
    assert List.objects.all().count() == 1
    assert Course.objects.all().count() == 1


@pytest.mark.django_db
def test_add_multiple_incorrect(client, test_user, add_courses):
    test_login(client, test_user)
    assert Course.objects.all().count() > 0

    response = client.post("/add_multiple_flashcards/",
                           {'list': ['1'], 'front_lang': ['1'], 'back_lang': ['1'], 'cards': ['Card1Cards2']})

    assert response.status_code == 404
    assert Flashcard.objects.all().count() == 0


@pytest.mark.django_db
def test_learning_mode_correct_answer(client, add_flashcard):
    assert Flashcard.objects.all().count() == 1
    card = Flashcard.objects.all().last()

    client.post(f"/learning_mode/{card.lists.first().id}/1/words/",
                {"card_id": [f"{card.id}"], "answer": [f"{card.back}"]})
    card = Flashcard.objects.all().last()
    assert card.mastery_level == 3


@pytest.mark.django_db
def test_learning_mode_incorrect_answer(client, add_flashcard):
    assert Flashcard.objects.all().count() == 1
    card = Flashcard.objects.all().last()

    client.post(f"/learning_mode/{card.lists.first().id}/1/words/",
                {"card_id": [f"{card.id}"], "answer": [""]})
    card = Flashcard.objects.all().last()
    assert card.mastery_level == 1


@pytest.mark.django_db
def test_anonymous_delete(client, add_flashcard):
    assert List.objects.all().count() == 1

    response = client.get('/delete/l/1')

    assert response.status_code != 200
