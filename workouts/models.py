from django.db import models
from django.urls.base import reverse
from users.models import BaseUser
# Create your models here.


class Exercise(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='tag')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ExerciseInstance(models.Model):
    workout = models.ForeignKey(
        "Workout", on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Exercise({self.exercise}, weight={self.weight})'


class Set(models.Model):
    instance = models.ForeignKey(
        'ExerciseInstance', on_delete=models.CASCADE, related_name="sets")
    repetitions = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Reps:{self.repetitions} {self.comment}'


class Workout(models.Model):
    user = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name="workouts")
    date = models.DateField(auto_now_add=True)
    types = models.ManyToManyField("WorkoutType", blank=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        name = self.date.strftime("%d/%m/%y")
        for type in self.types.all():
            name += f' {type}'
        return name

    def get_user_workouts(user):
        workouts = Workout.filter(user=user)
        return workouts

    def get_absolute_url(self):
        return reverse('detail-workout', kwargs={'pk': self.id})


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    exercises = models.ManyToManyField(Exercise, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkoutType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    workouts = models.ManyToManyField(Workout, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
