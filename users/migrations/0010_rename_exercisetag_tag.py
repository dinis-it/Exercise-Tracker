# Generated by Django 3.2.5 on 2021-10-08 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20211008_1540'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExerciseTag',
            new_name='Tag',
        ),
    ]
