import random
import re
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from flashcards.forms import AddFlashcard, AddList, AddCourse, AddLanguage, LoginForm, CreateNewUserForm
from flashcards.models import Flashcard, Language, List, Course
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


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


class AddFlashcardView(LoginRequiredMixin, View):
    login_url = 'login'

    # Allows to add a new flashcard using AddFlashcard form
    def get(self, request):
        form = AddFlashcard()
        return render(request, 'add-flashcard.html', {"form": form})

    def post(self, request):
        form = AddFlashcard(data=request.POST, files=request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('/show_all/flashcards/')
        else:
            return HttpResponse("Error")


class AddMultipleFlashcardsView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        lists = List.objects.all()
        langs = Language.objects.all()
        ctx = {
            "lists": lists,
            "langs": langs
        }
        return render(request, "add-multiple-flashcards.html", ctx)

    def post(self, request):
        cards = request.POST.get("cards")
        chosen_list = get_object_or_404(List, id=request.POST.get("list"))
        front_lang = get_object_or_404(Language, id=request.POST.get("front_lang"))
        back_lang = get_object_or_404(Language, id=request.POST.get("back_lang"))
        x = re.findall(";\s+\w", cards)
        if not cards or len(x) == 0:
            messages.error(request, "Typed cards' content is invalid!")
            return redirect("/add_multiple_flashcards/")

        new_cards = cards.split("\r\n")
        for card in new_cards:
            new_card = card.split("; ")
            flashcard = Flashcard()
            flashcard.front = new_card[0]
            flashcard.back = new_card[1]
            flashcard.front_language = front_lang
            flashcard.back_language = back_lang
            flashcard.save()
            flashcard.lists.add(chosen_list)
        return redirect("/show_all/flashcards/")


class ShowAllFlashcardsView(View):
    def get(self, request):
        flashcards = Flashcard.objects.all().order_by("id")
        return render(request, 'show-all-flashcards.html', {"flashcards": flashcards})


class FlashcardDetailView(View):
    def get(self, request, pk):
        card = get_object_or_404(Flashcard, id=pk)
        return render(request, 'flashcard-details.html', {"card": card})


class EditFlashcardView(LoginRequiredMixin, View):
    login_url = 'login'

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
        form = AddFlashcard(data=request.POST, instance=card, files=request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect(f"/show_all/flashcards/{card.id}")
        else:
            return HttpResponse("Error!")


class DeleteFlashcardView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        card = get_object_or_404(Flashcard, id=pk)
        card.delete()
        return redirect("/show_all/lists")


class RedirectDeleteFlashcardView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        item = get_object_or_404(Flashcard, id=pk)
        item.delete()
        return redirect(request.META['HTTP_REFERER'])


class ShowListsView(View):
    def get(self, request):
        lists = List.objects.all().order_by("id")
        return render(request, 'show_lists.html', {"lists": lists})


class ListDetailView(View):
    def get(self, request, pk):
        list = get_object_or_404(List, id=pk)
        return render(request, 'list-details.html', {"list": list})


class AddListView(LoginRequiredMixin, View):
    login_url = 'login'

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


class EditListView(LoginRequiredMixin, View):
    login_url = 'login'

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


class AddFlashcardToListView(LoginRequiredMixin, View):
    login_url = 'login'

    # Allows to add a new flashcard using AddFlashcard form to a specific list
    def get(self, request, pk):
        adding_to_list = get_object_or_404(List, id=pk)
        form = AddFlashcard(initial={"lists": adding_to_list,
                                     "front_language": adding_to_list.language_to_learn,
                                     "back_language": adding_to_list.learning_in_language})
        return render(request, 'add-flashcard.html', {"form": form})

    def post(self, request, pk):
        form = AddFlashcard(data=request.POST, files=request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect(f'/show_all/lists/{pk}')
        else:
            return HttpResponse("Error")


class DeleteListView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        list_to_delete = get_object_or_404(List, id=pk)
        list_to_delete.delete()
        return redirect("/show_all/lists/")


class RedirectDeleteListView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        item = get_object_or_404(List, id=pk)
        item.delete()
        return redirect(request.META['HTTP_REFERER'])


class ShowCoursesView(View):
    def get(self, request):
        courses = Course.objects.all().order_by("id")
        return render(request, "show-courses.html", {"courses": courses})


class CourseDetailView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        return render(request, 'course-details.html', {"course": course})


class AddCourseView(LoginRequiredMixin, View):
    login_url = 'login'

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


class EditCourseView(LoginRequiredMixin, View):
    login_url = 'login'

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


class AddListToCourseView(LoginRequiredMixin, View):
    login_url = 'login'

    # Allows to add a new list using AddList form to a specific course
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        form = AddList(initial={"courses": course,
                                "language_to_learn": course.language_to_learn,
                                "learning_in_language": course.learning_in_language})
        return render(request, 'add-list.html', {"form": form})

    def post(self, request, pk):
        form = AddList(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/show_all/courses/{pk}')
        else:
            return HttpResponse("Error")


class DeleteCourseView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        course.delete()
        return redirect("/show_all/courses/")


class RedirectDeleteView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, cls, pk):
        if cls == "c":
            item = get_object_or_404(Course, id=pk)
        elif cls == "f":
            item = get_object_or_404(Flashcard, id=pk)
        else:
            item = get_object_or_404(List, id=pk)
        item.delete()
        return redirect(request.META['HTTP_REFERER'])


class LearningModeMainView(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, "learning-mode-main.html", {"courses": courses})


class CourseLearningModeView(View):
    def get(self, request, pk):
        if 'card_id' in request.session:
            del request.session['card_id']
        course = get_object_or_404(Course, id=pk)
        ctx = {
            'course': course,
        }
        return render(request, "course-learning-mode.html", ctx)

    def post(self, request, pk):
        chosen_list_id = request.POST.get("list")
        level = request.POST.get("level")
        method = request.POST.get("method")
        if chosen_list_id == "" or level == "":
            messages.error(request, "Please choose a list and a level")
            return redirect(f"/learning_mode/course/{pk}/")
        else:
            return redirect(f"/learning_mode/{chosen_list_id}/{level}/{method}/")


class FlashcardGame(View):
    def get(self, request, pk, level, method):
        if pk[0] == "c":
            course_lists = List.objects.filter(courses_id=pk[1:])
            cards_list = []
            for el in course_lists:
                if level == 5:
                    if el.flashcard_set.filter(is_difficult=True):
                        cards_list.append(el.flashcard_set.filter(is_difficult=True))
                else:
                    if el.flashcard_set.filter(mastery_level=level):
                        cards_list.append(el.flashcard_set.filter(mastery_level=level))
            if len(cards_list) == 0:
                messages.error(request, "No such cards!")
                return redirect(f"/learning_mode/course/{pk[1:]}/")

            cards = cards_list[-1]
            for i in range(len(cards_list) - 1):
                cards = cards | cards_list[i]

        else:
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
                    return redirect(f"/learning_mode/course/{chosen_list.courses.id}/")

        if level == 1 or level == 4 or level == 5:
            print(request.session["card_id"]) if "card_id" in request.session else print("None")

            if "card_id" in request.session:
                condition_1 = int(request.session["card_id"]) not in list(
                    cards.all().values_list('id', flat=True)) and level in [1, 4]
                condition_2 = int(request.session["card_id"]) in list(cards.all().values_list('id', flat=True))

                if condition_1 or condition_2:
                    if cards.order_by("id").filter(id__lt=request.session['card_id']).count() != 0:
                        random_card = cards.order_by("id").filter(id__lt=request.session['card_id']).last()
                    else:
                        messages.success(request, f"Revised all cards on this mastery level!")
                        card = get_object_or_404(Flashcard, id=request.session["card_id"])
                        del request.session['card_id']
                        return redirect(f"/learning_mode/course/{card.lists.first().courses.id}/")

                else:
                    random_card = cards.order_by("id").last()

            else:
                random_card = cards.order_by("id").last()

        else:
            random_card = random.choice(cards)
        ctx = {
            "card": random_card,
            "method": method
        }
        return render(request, "flashcard-game.html", ctx)

    def course_all(self, request, pk, level, method):
        if pk[0] != "c":
            chosen_list = get_object_or_404(List, id=pk)
            if level != 5 and chosen_list.flashcard_set.filter(mastery_level=level):
                return redirect(f"/learning_mode/{pk}/{level}/{method}/")
            elif level == 5 and chosen_list.flashcard_set.filter(is_difficult=True):
                return redirect(f"/learning_mode/{pk}/{level}/{method}/")
            else:
                messages.success(request, f"Revised all cards on this mastery level!")
                del request.session['card_id']
                return redirect(f"/learning_mode/course/{chosen_list.courses.id}/")
        else:
            if level != 5:
                if Flashcard.objects.filter(lists__courses_id=pk[1:]).filter(mastery_level=level):
                    return redirect(f"/learning_mode/{pk}/{level}/{method}/")
            elif level == 5:
                if Flashcard.objects.filter(lists__courses_id=pk[1:]).filter(is_difficult=True):
                    return redirect(f"/learning_mode/{pk}/{level}/{method}/")
            else:
                messages.success(request, f"Revised all cards on this mastery level!")
                del request.session['card_id']
                return redirect(f"/learning_mode/course/{pk[1:]}/")

    def post(self, request, pk, level, method):
        answer = request.POST.get("answer").lower()
        card_id = request.POST.get("card_id")
        card = Flashcard.objects.get(id=card_id)
        if method == "img" or method == "words-reverse":
            result = True if answer == card.front.lower() else False
        else:
            result = True if answer == card.back.lower() else False

        if result:
            if card.mastery_level < 4:
                card.mastery_level = card.mastery_level + 1
                card.save()
            messages.success(request, f"Correct answer!")
            request.session['card_id'] = card_id
            return self.course_all(request, pk, level, method)
        else:
            if card.mastery_level > 1:
                card.mastery_level = card.mastery_level - 1
                card.save()
            if method == "words":
                messages.error(request, f"Wrong Answer! The correct answer was {card.back}.")
            else:
                messages.error(request, f"Wrong Answer! The correct answer was {card.front}.")
            request.session['card_id'] = card_id
            return self.course_all(request, pk, level, method)


class AddLanguageView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = AddLanguage()
        return render(request, 'add-language.html', {"form": form})

    def post(self, request):
        form = AddLanguage(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/show_all/courses/add/')
        else:
            return HttpResponse("Error!")


class EditLanguagesView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        languages = Language.objects.all().order_by("id")
        return render(request, "edit-languages.html", {"languages": languages})

    def post(self, request):
        language_id = request.POST.get("language")
        return redirect(f"/edit_languages/{language_id}/")


class EditLanguageDetailView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        language = get_object_or_404(Language, id=pk)
        form = AddLanguage(instance=language)
        ctx = {
            "language": language,
            "form": form
        }
        return render(request, "edit-language-details.html", ctx)

    def post(self, request, pk):
        language = get_object_or_404(Language, id=pk)
        form = AddLanguage(request.POST, instance=language)
        if form.is_valid():
            form.save()
        return redirect("/edit_languages/")


class DeleteLanguageView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, pk):
        language = get_object_or_404(Language, id=pk)
        language.delete()
        return redirect("/edit_languages/")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login-form.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, 'Failed to log in!')
                return redirect("/login/")
        else:
            return render(request, 'login-form.html', {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class CreateNewUserView(View):
    def get(self, request):
        form = CreateNewUserForm()
        return render(request, 'register-form.html', {"form": form})

    def post(self, request):
        form = CreateNewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request, 'register-form.html', {"form": form})
