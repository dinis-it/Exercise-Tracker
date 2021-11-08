from django.urls.conf import path
from .views import (
    CreateExercise,
    Workouts,
    CreateWorkout,
    CreateType,
    CreateTag,
    add_set,
    detail_workout,
    render_list,
    add_instance,
    edit_instance,
    delete_instance,
    delete_set,
    edit_set,
)

urlpatterns = [
    path('', Workouts.as_view(), name='workouts'),
    path('add/', CreateWorkout.as_view(), name='add-workout'),
    path('types/add/', CreateType.as_view(), name='add-type'),
    path('tags/add', CreateTag.as_view(), name='add-tag'),
    path('exercises/add', CreateExercise.as_view(), name='add-exercise'),
    path('<int:pk>/list', render_list, name='load-list'),
    path('<int:pk>/edit', detail_workout, name='detail-workout'),
    path('<int:pk>/instances/add', add_instance, name='add-instance'),
    path('instances/<int:pk>/edit', edit_instance, name='edit-instance'),
    path('instances/<int:pk>/delete', delete_instance, name='delete-instance'),
    path('instances/<int:pk>/sets/add', add_set, name='add-set'),
    path('sets/<int:pk>/edit', edit_set, name='edit-set'),
    path('sets/<int:pk>/delete', delete_set, name='delete-set'),

]
