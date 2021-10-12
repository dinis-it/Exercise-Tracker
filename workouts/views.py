from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from workouts.forms import ExerciseForm, TypeForm, WorkoutForm, TagForm
from .models import (
    Exercise,
    Workout,
    WorkoutType,
    Tag,
)
# Create your views here.


class Workouts(LoginRequiredMixin, ListView):
    template_name = 'workouts/workouts.html'
    model = Workout
    context_object_name = 'workouts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.request.user.id)
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        # id = self.request.user.id
        exercises = Exercise.objects.all()
        types = WorkoutType.objects.all()
        tags = Tag.objects.all()
        context['exercises'] = exercises
        context['types'] = types
        context['tags'] = tags
        return context


class CreateWorkout(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'workouts/add_workout.html'
    form_class = WorkoutForm
    success_url = reverse_lazy('workouts')
    success_message = "New workout added"


class CreateType(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'workouts/add_type.html'
    form_class = TypeForm
    success_url = reverse_lazy('workouts')
    success_message = "Workout type %(name)s was created successfully"


class CreateExercise(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'workouts/add_exercise.html'
    form_class = ExerciseForm
    success_url = reverse_lazy('workouts')
    success_message = "Exercise %(name)s was created successfully"


class CreateTag(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'workouts/add_tag.html'
    form_class = TagForm
    success_url = reverse_lazy('workouts')
    success_message = "Tag %(name)s was created successfully"
