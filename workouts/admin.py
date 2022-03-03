from django.contrib import admin
from .models import *

# Register your models here.


class ExerciseInstanceInline(admin.TabularInline):
    model = ExerciseInstance


class WorkoutAdmin(admin.ModelAdmin):
    inlines = [
        ExerciseInstanceInline,
    ]

admin.site.register(Workout, WorkoutAdmin)
admin.site.register(WorkoutType)
admin.site.register(ExerciseInstance)
admin.site.register(Exercise)
admin.site.register(Tag)
admin.site.register(Set)
