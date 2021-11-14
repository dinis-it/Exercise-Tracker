from django.http.response import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from workouts.forms import DateTimeForm, InstanceForm, SetForm
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


@login_required()
def input_swap(request):
    if request.method == 'POST':
        if request.choice.value == 'type':
            return render(request, 'workouts/partials/input_text.html')
        else:
            return render(request, 'workouts/partials/input_date')


@login_required
def search_test(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        print('search', search)
        workouts = Workout.objects.filter(types__name__icontains=search)
        print(workouts)
        context = {
            'workouts': workouts
        }
        return render(request, 'workouts/partials/workout_list.html', context)


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
            return render(request, "workouts/partials/edit_instance.html", context)
    form = SetForm()
    context = {'form': form,
               'exercise': exercise, }
    return render(request, 'workouts/partials/add_set.html', context)


@login_required
def edit_set(request, pk):
    set = get_object_or_404(Set, pk=pk)
    if request.method == 'POST':
        form = SetForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("I'm valid")
            set.save()
            context = {
                'set': set,
                'exercise': set.instance,
            }
            return render(request, "workouts/partials/render.html", context)
    form = SetForm()
    context = {'form': form,
               'set': set, }
    return render(request, 'workouts/partials/edit_set.html', context)


@login_required
def delete_set(request, pk):
    if request.method == "DELETE":
        set = get_object_or_404(Set, pk=pk)
        set.delete()
        return HttpResponse('')


@login_required
def add_instance(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == 'POST':
        form = InstanceForm(request.POST)
        if form.is_valid():
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
            exercise = form.save(commit=False)
            exercise.id = instance.id
            exercise.workout_id = instance.workout_id
            exercise.save()
            context = {'form': form,
                       'exercise': instance,
                       'workout': instance.workout}
            return render(request, "workouts/partials/render.html", context)
        else:
            form = InstanceForm(instance=instance)
            context = {'form': form,
                       'exercise': instance,
                       'workout': instance.workout}
            return render(request, 'workouts/partials/edit_instance.html', context)
    context = {'form': form,
               'exercise': instance,
               'workout': instance.workout}
    return render(request, 'workouts/partials/edit_instance.html', context)


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
def delete_workout(request, pk):
    if request.method == "delete":
        workout = get_object_or_404(Workout, pk=pk)
        workout.delete()
        return HttpResponse("")


@login_required
def detail_workout(request, pk):
    user = request.user
    if request.method == "POST":
        workout = Workout.objects.create()
        workout.user = user
        workout.save()
        context = {'user': user,
                   'workout': workout}
        return render(request, 'workouts/detail_workout.html', context)

    workout = get_object_or_404(Workout, pk=pk)
    context = {'user': user,
               'workout': workout}

    return render(request, 'workouts/detail_workout.html', context)


def workouts(request):
    user = request.user
    if request.method == "POST":
        workout = Workout.objects.create(user=user)
        user.workouts.add(workout)
        context = {'user': user,
                   'workout': workout}
        return redirect('detail-workout', pk=workout.pk)

    workouts = get_list_or_404(Workout, user=user)
    exercises = get_list_or_404(Exercise)
    types = get_list_or_404(WorkoutType)
    tags = get_list_or_404(Tag)
    form = DateTimeForm()
    context = {'user': user,
               'workouts': workouts,
               'exercises': exercises,
               'types': types,
               'tags': tags,
               'form': form
               }
    return render(request, 'workouts/workouts.html', context)

 # Class-based views suck


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
