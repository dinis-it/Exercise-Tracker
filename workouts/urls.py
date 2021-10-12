from django.urls.conf import path
from .views import (
    CreateExercise,
    Workouts,
    CreateWorkout,
    CreateType,
    CreateTag,
)

urlpatterns = [
    path('', Workouts.as_view(), name='workouts'),
    path('add/', CreateWorkout.as_view(), name='add_workout'),
    path('types/add/', CreateType.as_view(), name='add_type'),
    path('tags/add', CreateTag.as_view(), name='add_tag'),
    path('exercises/add', CreateExercise.as_view(), name='add_exercise'),
]
