from django.http.response import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from workouts.forms import InstanceForm, SetForm
from workouts.forms import ExerciseForm, TypeForm, WorkoutForm, TagForm
from workouts.models import (
    Exercise,
    ExerciseInstance,
    Workout,
    WorkoutType,
    Tag,
    Set,
)
from users.models import BaseUser
# Create your views here.


@login_required
def add_set(request, pk):
    exercise = get_object_or_404(ExerciseInstance, pk=pk)
    if request.method == 'POST':
        form = SetForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("I'm valid")
            set = form.save(commit=False)
            set.instance = exercise
            set.save()
            context = {'exercise': exercise,
                       'workout': exercise.workout}
            return render(request, "workouts/partials/render.html", context)
    form = SetForm()
    context = {'form': form,
               'exercise': exercise, }
    return render(request, 'workouts/partials/add_set.html', context)


@login_required
def add_instance(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == 'POST':
        form = InstanceForm(request.POST)
        print("POST")
        print(request.POST)
        if form.is_valid():
            print("I'm valid")
            instance = form.save(commit=False)
            instance.workout = workout
            instance.save()
            context = {'exercise': instance,
                       'workout': instance.workout}
            return render(request, "workouts/partials/render.html", context)
        else:
            context = {'form': form,
                       'workout': workout}
            return render(request, 'workouts/partials/add_instance.html', context)
    form = InstanceForm()
    context = {'form': form,
               'workout': workout, }
    return render(request, 'workouts/partials/add_instance.html', context)


@login_required
def edit_instance(request, pk):
    instance = get_object_or_404(ExerciseInstance, pk=pk)

    form = InstanceForm(request.POST or None, instance=instance)
    if request.method == "POST":
        form = InstanceForm(request.POST)
        if form.is_valid():
            print("I'm valid")
            exercise = form.save(commit=False)
            exercise.id = instance.id
            exercise.workout_id = instance.workout_id
            exercise.save()
            context = {'exercise': instance,
                       'workout': instance.workout}
            return render(request, "workouts/partials/render.html", context)
        else:
            print("hi")
            form = InstanceForm(instance=instance)
            context = {'form': form,
                       'exercise': instance,
                       'workout': instance.workout}
            return render(request, 'workouts/partials/edit_instance.html', context)
    print("hey")
    context = {'form': form,
               'exercise': instance,
               'workout': instance.workout}
    return render(request, 'workouts/partials/edit_instance.html', context)


@login_required
def delete_set(request, pk):
    if request.method == "DELETE":
        set = get_object_or_404(Set, pk=pk)
        set.delete()
        return HttpResponse('')


@login_required
def delete_instance(request, pk):
    if request.method == "DELETE":
        instance = get_object_or_404(ExerciseInstance, pk=pk)
        instance.delete()
        return HttpResponse('')


@login_required
def render_list(request, pk):
    # Render a list of exercises in a particular workout
    workout = get_object_or_404(Workout, pk=pk)
    exercises = workout.exercises.all()
    context = {
        "exercises": exercises,
    }
    return render(request, "workouts/partials/instance_list.html", context)


@login_required
def detail_workout(request, pk):
    user = request.user
    workout = get_object_or_404(Workout, pk=pk)
    context = {'user': user,
               'workout': workout}

    return render(request, 'workouts/detail_workout.html', context)


class Workouts(LoginRequiredMixin, ListView):
    template_name = 'workouts/workouts.html'
    model = Workout
    context_object_name = 'workouts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.request.user.id)
        return queryset

    def get_context_data(self):
        user = self.request.user
        context = super().get_context_data()
        # id = self.request.user.id
        workouts = get_list_or_404(Workout, user=user)
        exercises = get_list_or_404(Exercise)
        types = get_list_or_404(WorkoutType)
        tags = get_list_or_404(Tag)
        context['workouts'] = workouts
        context['exercises'] = exercises
        context['types'] = types
        context['tags'] = tags
        return context


class CreateWorkout(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'workouts/add_workout.html'
    form_class = WorkoutForm
    success_url = reverse_lazy('workouts')
    success_message = "New workout added"

    def form_valid(self, form):
        workout = form.save(commit=False)
        workout.user = get_object_or_404(BaseUser, user=self.request.user)
        workout.save()
        redirect('edit_workout')


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
