from django.contrib import admin

# Register your models here.
from flashcards.models import List, Course, Language, Flashcard

admin.site.register(List)
admin.site.register(Flashcard)
admin.site.register(Course)
admin.site.register(Language)

