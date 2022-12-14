"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from flashcards.views import MainView, AddFlashcardView, ShowAllFlashcardsView, FlashcardDetailView, EditFlashcardView, DeleteFlashcardView, ShowListsView, ListDetailView, AddListView, EditListView, AddFlashcardToListView, DeleteListView, ShowCoursesView, CourseDetailView, AddCourseView, EditCourseView, DeleteCourseView, AddListToCourseView, LearningModeMainView, CourseLearningModeView, FlashcardGame, AddLanguageView, RedirectDeleteView, LoginView, LogoutView, CreateNewUserView, EditLanguagesView, EditLanguageDetailView, DeleteLanguageView, AddMultipleFlashcardsView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', CreateNewUserView.as_view(), name="register"),
    path('add_flashcard/', AddFlashcardView.as_view(), name="add-flashcard"),
    path('add_multiple_flashcards/', AddMultipleFlashcardsView.as_view(), name="add-multiple"),
    path('show_all/flashcards/', ShowAllFlashcardsView.as_view(), name='list-flashcards'),
    path('show_all/flashcards/<int:pk>/', FlashcardDetailView.as_view(), name='flashcard-details'),
    path('show_all/flashcards/<int:pk>/edit/', EditFlashcardView.as_view(), name='edit-flashcard'),
    path('show_all/flashcards/<int:pk>/delete/', DeleteFlashcardView.as_view(), name='delete-flashcard'),
    path('show_all/lists/', ShowListsView.as_view(), name='show-lists'),
    path('show_all/lists/<int:pk>/', ListDetailView.as_view(), name="list-details"),
    path('add_list/', AddListView.as_view(), name="add-list"),
    path('show_all/lists/<int:pk>/edit/', EditListView.as_view(), name='edit-list'),
    path('show_all/lists/<int:pk>/add-flashcard/', AddFlashcardToListView.as_view(), name='add-flashcard-to-list'),
    path('show_all/lists/<int:pk>/delete/', DeleteListView.as_view(), name="delete-list"),
    path('show_all/courses/', ShowCoursesView.as_view(), name="show-courses"),
    path('show_all/courses/<int:pk>/', CourseDetailView.as_view(), name="course-details"),
    path('show_all/courses/add/', AddCourseView.as_view(), name="add-course"),
    path('show_all/courses/<int:pk>/edit/', EditCourseView.as_view(), name="edit-course"),
    path('show_all/courses/<int:pk>/delete/', DeleteCourseView.as_view(), name="delete-course"),
    path('show_all/courses/<int:pk>/add-list/', AddListToCourseView.as_view(), name="add-list-to-course"),
    path('learning_mode/', LearningModeMainView.as_view(), name="learning-mode"),
    path('learning_mode/course/<int:pk>/', CourseLearningModeView.as_view(), name="course-learning-mode"),
    path('learning_mode/<str:pk>/<int:level>/<str:method>/', FlashcardGame.as_view(), name="flashcard-game"),
    path('add_language/', AddLanguageView.as_view(), name="add-language"),
    path('edit_languages/', EditLanguagesView.as_view(), name="edit-languages"),
    path('edit_languages/<int:pk>/', EditLanguageDetailView.as_view(), name="edit-language-details"),
    path('delete_language/<int:pk>/', DeleteLanguageView.as_view(), name="delete-language"),
    path('delete/<str:cls>/<int:pk>/', RedirectDeleteView.as_view(), name='redirect-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
