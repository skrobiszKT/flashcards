from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from flashcards.models import Flashcard, Language, MASTERY_LEVELS, List, Course


# class AddFlashcard(forms.Form):
#     front = forms.CharField(label="Front")
#     front_language = forms.ChoiceField(label="Front Language", choices=Language.objects.all(), required=False)
#     back = forms.CharField(label="Back")
#     back_language = forms.ChoiceField(label="Back Language", choices=Language.objects.all(), required=False)
#     mastery_level = forms.ChoiceField(label="Mastery Level", choices=MASTERY_LEVELS)
#     is_difficult = forms.BooleanField(label="Difficult", required=False)
#     tags = forms.CharField(label="Tags (separated by comma)", required=False)

class AddFlashcard(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddFlashcard, self).__init__(*args, **kwargs)
        self.fields['front_language'].required = False
        self.fields['back_language'].required = False
        self.fields['tags'].required = False
        self.fields['image'].required = False


class AddList(forms.ModelForm):
    class Meta:
        model = List
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddList, self).__init__(*args, **kwargs)
        self.fields['language_to_learn'].required = False
        self.fields['learning_in_language'].required = False
        self.fields['tags'].required = False
        self.fields['courses'].required = True


class AddCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddCourse, self).__init__(*args, **kwargs)
        self.fields['language_to_learn'].required = False
        self.fields['learning_in_language'].required = False
        self.fields['tags'].required = False


class AddLanguage(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'

    def __int__(self, *args, **kwargs):
        super(AddLanguage, self).__init__(*args, **kwargs)
        self.fields['symbol'].required = False


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, max_length=50)


class CreateNewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
