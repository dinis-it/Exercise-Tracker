from django import forms
from django.forms import ModelForm
from django.forms.forms import Form
from django.forms.models import inlineformset_factory
from .models import (
    ExerciseInstance,
    Set,
    Workout,
    Exercise,
    Tag,
    WorkoutType,
)


class WorkoutForm(ModelForm):

    class Meta:
        model = Workout
        exclude = ['user', 'comments']


class ExerciseForm(ModelForm):

    class Meta:
        model = Exercise
        fields = '__all__'


class SetForm(ModelForm):

    class Meta:
        model = Set
        exclude = ['instance']


class InstanceForm(ModelForm):

    class Meta:
        model = ExerciseInstance
        exclude = ['workout']


class TagForm(ModelForm):

    class Meta:
        model = Tag
        fields = ['name']


class TypeForm(ModelForm):

    class Meta:
        model = WorkoutType
        fields = ['name']
