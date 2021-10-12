from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import (
    ExerciseInstance,
    Set,
    Workout,
    Exercise,
    Tag,
    WorkoutType,
)


InstanceFormset = inlineformset_factory()


class WorkoutForm(ModelForm):

    class Meta:
        model = Workout
        exclude = ['user']


class ExerciseForm(ModelForm):

    class Meta:
        model = Exercise
        fields = '__all__'


class SetForm(ModelForm):

    class Meta:
        model = Set
        fields = '__all__'


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
