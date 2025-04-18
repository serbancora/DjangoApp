from django.contrib import admin
from .models import Ierarhie, Lectie, Flashcard, ReviewState

# Register your models here.

admin.site.register(Ierarhie)
admin.site.register(Lectie)
admin.site.register(Flashcard)
admin.site.register(ReviewState)