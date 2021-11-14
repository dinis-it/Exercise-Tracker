from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from users.models import BaseUser, Profile, Weight
from django import forms

# Users


class RegistrationForm(UserCreationForm):

    class Meta:
        model = BaseUser
        fields = ['username', 'password1', 'password2', 'email']


class PasswordUpdateForm(PasswordChangeForm):
    model = BaseUser


class UserUpdateForm(ModelForm):

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ['user']

class WeightForm(ModelForm):
    
    class Meta:
        model=Weight
        exclude = ['user']