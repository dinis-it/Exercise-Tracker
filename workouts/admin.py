from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Workout)
admin.site.register(WorkoutType)
admin.site.register(ExerciseInstance)
admin.site.register(Exercise)
admin.site.register(Tag)
admin.site.register(Set)