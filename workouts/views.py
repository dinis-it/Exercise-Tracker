from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

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
def add_type(request):
    '''Handle a form for creating workout types'''
    form = TypeForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            context = {
                'form': form
            }
            return render(request, 'workouts/partials/add_type.html', context)
    context = {
        'form': form
    }
    return render(request, 'workouts/partials/add_type.html', context)


@login_required
def workouts(request):
    '''Main workout page, display a searchable list of workouts'''
    user = request.user
    if request.method == "POST":
        workout = Workout.objects.create(user=user)
        user.workouts.add(workout)
        context = {'user': user,
                   'workout': workout}
        return redirect('detail-workout', pk=workout.pk)

    workouts = get_list_or_404(Workout, user=user)
    paginator = Paginator(workouts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'user': user,
               'workouts': workouts,
               'page_obj': page_obj,
               }
    return render(request, 'workouts/workouts.html', context)


@login_required
def search_exercise(request):
    '''Display a list of workouts which contain exercises matching (fully or partially) the user's search box input'''
    # name must match, user must match
    user = request.user
    if request.method == 'POST':
        search = request.POST.get('search_exercise')
        if search == "":
            workouts = get_list_or_404(Workout, user=user)
            context = {'workouts': workouts}
            return render(request, 'workouts/partials/workout_list.html', context)
        else:
            exercises = ExerciseInstance.objects.filter(
                exercise__name__icontains=search).filter(workout__user__exact=user)
            context = {
                'exercises': exercises
            }
        return render(request, 'workouts/partials/exercise_list.html', context)


@login_required
def search_workout(request):
    '''Display a list of workouts which contain types matching (fully or partially) the user's search box input'''
    if request.method == 'POST':
        search = request.POST.get('search_workout')

        workouts = Workout.objects.filter(types__name__icontains=search)
        context = {
            'workouts': workouts
        }
        return render(request, 'workouts/partials/workout_list.html', context)


@login_required
def add_set(request, pk):
    exercise = get_object_or_404(ExerciseInstance, pk=pk)
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
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
def save_instance_and_add_set(request, pk):
    ''' Save an exercise instance and return an edit form and an extra set form '''
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == "POST":
        form = InstanceForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.workout = workout
            set_form = SetForm()
            context = {
                workout: workout,
                form: form,
                set_form: set_form
            }
            return render(request, 'workouts/partials/add_instance_set.html', context)
        context = {
            workout: workout,
            form: form
        }
        return render(request, 'workouts/partials/add_instance.html', context)


@login_required
def edit_set(request, pk):
    ''' '''
    set = get_object_or_404(Set, pk=pk)
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            set.save()
            context = {
                'set': set,
                'exercise': set.instance,
            }
            response = HttpResponse()
            response['HX-Trigger'] = "refreshList"
            return response
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
    '''Add a form for creating an instance of an exercise, display on the workout detail page directly'''
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == 'POST':
        form = InstanceForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.workout = workout
            instance.save()
            response = HttpResponse()
            # HTMX event trigger for rerendering the instance list
            response['HX-Trigger'] = "refreshList"
            return response
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
    '''Edit an instance and re-render exercise list'''
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
            response = HttpResponse()
            response['HX-Trigger'] = "refreshList"
            return response
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
    '''Delete an exercise instance'''
    if request.method == "DELETE":
        instance = get_object_or_404(ExerciseInstance, pk=pk)
        instance.delete()
        response = HttpResponse()
        response['HX-Trigger'] = "refreshList"
        return response


@login_required
def render_list(request, pk):
    """Render a list of exercises for a particular workout"""
    workout = get_object_or_404(Workout, pk=pk)
    exercises = workout.exercises.all()
    context = {
        "workout": workout,
        "exercises": exercises,
    }
    return render(request, "workouts/partials/instance_list.html", context)


@login_required
def edit_workout(request):
    '''Display a modal for selecting workout types and adding comments'''
    user = request.user
    form = WorkoutForm(request.POST or None)
    if request.method == "POST":
        workout = Workout.objects.create(user=user)
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            workout = form.save()
            instance_form = InstanceForm()
            context = {
                'workout': workout,
                'form': instance_form,
            }
            # Render an instance form inside the workout modal
            return redirect(workout)
    context = {'form': form}
    return render(request, 'workouts/partials/edit_workout.html', context)


@login_required
def add_workout(request):
    '''Display a modal with a form to handle workout creation'''
    user = request.user
    form = WorkoutForm(request.POST or None)
    if request.method == "POST":
        workout = Workout.objects.create(user=user)
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            workout = form.save()
            instance_form = InstanceForm()
            context = {
                'workout': workout,
                'form': instance_form,
            }
            return redirect(workout)
    context = {'form': form}
    return render(request, 'workouts/partials/edit_workout.html', context)


@login_required
def detail_workout(request, pk):
    '''Display details of a workout'''
    user = request.user
    workout = get_object_or_404(Workout, pk=pk)
    form = WorkoutForm(instance=workout)
    context = {
        'user': user,
        'workout': workout,
        'form': form,
    }

    response = render(request, 'workouts/detail_workout.html', context)
    response['HX-Trigger'] = "refreshList"
    return response


@login_required
def delete_workout(request, pk):
    '''Delete a given workout'''
    user = request.user
    if request.method == "DELETE":
        workout = get_object_or_404(Workout, pk=pk)
        workout.delete()
        workouts = get_list_or_404(Workout, user=user)
        context = {'workouts': workouts}
        return HttpResponse("")
        # return render(request, 'workouts/partials/workout_list.html', context)


def add_exercise(request):
    '''Display a form for adding exercises to the exercise list'''
    form = ExerciseForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponse("")
    context = {'form': form}
    return render(request, 'workouts/partials/add_exercise.html', context)


# Class-based views

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
        redirect('detail_workout')


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
