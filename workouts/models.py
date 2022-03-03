from django.db import models
from django.urls.base import reverse
from django.shortcuts import get_list_or_404
from users.models import BaseUser
# Create your models here.


class Exercise(models.Model):
    name = models.CharField(max_length=100, primary_key=True, unique=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='tag')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Set(models.Model):
    instance = models.ForeignKey(
        'ExerciseInstance', on_delete=models.CASCADE, related_name="sets")
    repetitions = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Reps:{self.repetitions}'


class ExerciseInstance(models.Model):
    workout = models.ForeignKey(
        "Workout", on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Exercise({self.exercise}, weight={self.weight})'

    # def format_sets(self):
    #     sets = Set.objects.filter(instance=self)
    #     if not sets:
    #         return ""
    #     reps = sets[0]
    #     if any(sets):
    #         print("none")
    #     if (not any(x != reps for x in sets)) and not any(sets):
    #         return f'{len(sets)} x {sets[0]}'
    #     else:
    #         output = ""
    #         for set in sets:
    #             if set.repetitions == None:
    #                 output += ""
    #             else:
    #                 output += str(set.repetitions) + " "
    #         return output

    def get_duration(self):
        if self.duration:
            return self.duration
        return "-"

    def get_weight(self):
        if self.weight:
            return self.weight
        return "-"

    def get_sets(self):
        sets = len(Set.objects.filter(instance=self))
        if not sets:
            return "-"
        return sets

    def get_comments(self):
        if self.comment:
            return self.comment
        return "-"

    def repetitions(self):
        repetitions = [
            set.repetitions for set in Set.objects.filter(instance=self)]
        return repetitions


class Workout(models.Model):
    user = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name="workouts")
    date = models.DateField(auto_now_add=True)
    types = models.ManyToManyField("WorkoutType", blank=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        name = self.date.strftime("%d/%m/%y")
        for type in self.types.all():
            name += f' - {type}'
        return name

    def has_exercises(self):
        exercises = ExerciseInstance.objects.filter(workout=self)
        return exercises

    def get_user_workouts(self):
        workouts = Workout.filter(user=self.user)
        return workouts

    def get_absolute_url(self):
        return reverse('detail-workout', kwargs={'pk': self.id})

    def get_date(self):
        return self.date.strftime("%d/%m/%y")

    def get_total_duration(self):
        # TODO implement logic for this
        total_duration = 0

    def get_total_sets(self):
        total_sets = 0
        exercises = self.exercises.all()
        for exercise in exercises:
            sets = exercise.sets.all()
            if any(set.repetitions != None for set in sets):
                total_sets += len(sets)
                sets = 0
        return total_sets

    def get_total_volume(self):
        total_volume = 0
        exercises = self.exercises.all()
        for exercise in exercises:
            if exercise.weight:
                sets = exercise.sets.all()
                for set in sets:
                    if set.repetitions != None:
                        total_volume += set.repetitions*exercise.weight
        return total_volume


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
