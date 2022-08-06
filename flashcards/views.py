import random

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, get_list_or_404
from django.views import View
from django.contrib import messages
from flashcards.forms import AddFlashcard, AddList, AddCourse
from flashcards.models import Flashcard, Language, List, Course


class MainView(View):
    # Main page View
    def get(self, request):
        if Flashcard.objects.all():
            random_card = random.choice(Flashcard.objects.all())
        else:
            random_card = None
        recent_course = Course.objects.order_by("-id").first()
        recent_list = List.objects.order_by("-id").first()
        ctx = {
            "card": random_card,
            "recent_course": recent_course,
            "recent_list": recent_list
        }
        return render(request, 'main.html', ctx)


class AddFlashcardView(View):
    # Allows to add a new flashcard using AddFlashcard form
    def get(self, request):
        form = AddFlashcard()
        return render(request, 'add-flashcard.html', {"form": form})

    def post(self, request):
        form = AddFlashcard(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/show_all/flashcards/')
        else:
            return HttpResponse("Error")


class ShowAllFlashcardsView(View):
    def get(self, request):
        flashcards = Flashcard.objects.all()
        return render(request, 'show-all-flashcards.html', {"flashcards": flashcards})


class FlashcardDetailView(View):
    def get(self, request, pk):
        card = get_object_or_404(Flashcard, id=pk)
        return render(request, 'flashcard-details.html', {"card": card})


class EditFlashcardView(View):
    def get(self, request, pk):
        card = get_object_or_404(Flashcard, id=pk)
        form = AddFlashcard(instance=card)
        ctx = {
            "form": form,
            "card": card
        }
        return render(request, 'edit-flashcard.html', ctx)

    def post(self, request, pk):
        card = get_object_or_404(Flashcard, id=pk)
        form = AddFlashcard(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect(f"/show_all/flashcards/{card.id}")
        else:
            return HttpResponse("Error!")


class DeleteFlashcardView(View):
    def get(self, request, pk):
        card = get_object_or_404(Flashcard, id=pk)
        card.delete()
        return redirect("/show_all/flashcards/")


class ShowListsView(View):
    def get(self, request):
        lists = List.objects.all()
        return render(request, 'show_lists.html', {"lists": lists})


class ListDetailView(View):
    def get(self, request, pk):
        list = get_object_or_404(List, id=pk)
        return render(request, 'list-details.html', {"list": list})


class AddListView(View):
    def get(self, request):
        form = AddList()
        return render(request, 'add-list.html', {"form": form})

    def post(self, request):
        form = AddList(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/show_all/lists/")
        else:
            return HttpResponse("Error")


class EditListView(View):
    def get(self, request, pk):
        list_to_edit = get_object_or_404(List, id=pk)
        form = AddList(instance=list_to_edit)
        ctx = {
            "list": list_to_edit,
            "form": form
        }
        return render(request, "edit-list.html", ctx)

    def post(self, request, pk):
        list_to_edit = get_object_or_404(List, id=pk)
        form = AddList(request.POST, instance=list_to_edit)
        if form.is_valid():
            form.save()
            return redirect(f"/show_all/lists/{list_to_edit.id}")
        else:
            HttpResponse("Error")


class AddFlashcardToListView(View):
    # Allows to add a new flashcard using AddFlashcard form to a specific list
    def get(self, request, pk):
        adding_to_list = get_object_or_404(List, id=pk)
        form = AddFlashcard(initial={"lists": adding_to_list,
                                           "front_language": adding_to_list.language_to_learn,
                                           "back_language": adding_to_list.learning_in_language})
        return render(request, 'add-flashcard.html', {"form": form})

    def post(self, request, pk):
        form = AddFlashcard(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/show_all/lists/{pk}')
        else:
            return HttpResponse("Error")


class DeleteListView(View):
    def get(self, request, pk):
        list_to_delete = get_object_or_404(List, id=pk)
        list_to_delete.delete()
        return redirect("/show_all/lists/")


class ShowCoursesView(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, "show-courses.html", {"courses": courses})


class CourseDetailView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        return render(request, 'course-details.html', {"course": course})


class AddCourseView(View):
    def get(self, request):
        form = AddCourse()
        return render(request, 'add-course.html', {"form": form})

    def post(self, request):
        form = AddCourse(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/show_all/courses/")
        else:
            return HttpResponse("Error")


class EditCourseView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        form = AddCourse(instance=course)
        ctx = {
            "course": course,
            "form": form
        }
        return render(request, "add-course.html", ctx)

    def post(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        form = AddCourse(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect(f"/show_all/courses/{course.id}")
        else:
            HttpResponse("Error")


class AddListToCourseView(View):
    # Allows to add a new list using AddList form to a specific course
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        form = AddList(initial={"courses": course,
                                           "language_to_learn": course.language_to_learn,
                                           "learning_in_language": course.learning_in_language})
        return render(request, 'add-course.html', {"form": form})

    def post(self, request, pk):
        form = AddList(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/show_all/courses/{pk}')
        else:
            return HttpResponse("Error")


class DeleteCourseView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        course.delete()
        return redirect("/show_all/courses/")


class LearningModeMainView(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, "learning-mode-main.html", {"courses": courses})


class CourseLearningModeView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        ctx = {
            'course': course,
        }
        return render(request, "course-learning-mode.html", ctx)

    def post(self, request, pk):
        chosen_list_id = request.POST.get("list")
        level = request.POST.get("level")
        if chosen_list_id == "" or level == "":
            messages.error(request, "Please choose a list and a level")
            return redirect(f"/learning_mode/course/{pk}/")
        else:
            return redirect(f"/learning_mode/{chosen_list_id}/{level}/")


class FlashcardGame(View):
    def get(self, request, pk, level):
        chosen_list = get_object_or_404(List, id=pk)
        if level == 5:
            if chosen_list.flashcard_set.filter(is_difficult=True):
                cards = chosen_list.flashcard_set.filter(is_difficult=True)
            else:
                messages.error(request, "No such cards!")
                return redirect("/learning_mode/")
        else:
            if chosen_list.flashcard_set.filter(mastery_level=level):
                cards = chosen_list.flashcard_set.filter(mastery_level=level)
            else:
                messages.error(request, "No such cards!")
                return redirect("/learning_mode/")
        random_card = random.choice(cards)
        return render(request, "flashcard-game.html", {"card": random_card})

    def post(self, request, pk, level):
        answer = request.POST.get("answer").lower()
        card_id = request.POST.get("card_id")
        card = Flashcard.objects.get(id=card_id)
        chosen_list = get_object_or_404(List, id=pk)
        if answer == card.back.lower():
            if card.mastery_level < 4:
                card.mastery_level = card.mastery_level + 1
                card.save()
            messages.success(request, f"Correct answer!")
            if chosen_list.flashcard_set.filter(mastery_level=level):
                return redirect(f"/learning_mode/{pk}/{level}/")
            else:
                messages.success(request, f"Revised all cards on this mastery level!")
                return redirect(f"/learning_mode/course/{chosen_list.courses.id}/")
        else:
            if card.mastery_level > 1:
                card.mastery_level = card.mastery_level - 1
                card.save()
            messages.error(request, f"Wrong Answer! The correct answer was {card.back}.")
            if chosen_list.flashcard_set.filter(mastery_level=level):
                return redirect(f"/learning_mode/{pk}/{level}/")
            else:
                messages.success(request, f"Revised all cards on this mastery level!")
                return redirect(f"/learning_mode/course/{chosen_list.courses.id}/")

