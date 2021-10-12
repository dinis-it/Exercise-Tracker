
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView, View

from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from users.forms import ProfileUpdateForm, RegistrationForm, UserUpdateForm
from users.models import BaseUser
from workouts.models import Workout


class UpdatePassword(LoginRequiredMixin, UpdateView):
    template_name = 'users/update_password.html'
    model = BaseUser
    form_class = PasswordChangeForm

    def get_object(self):
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        form = PasswordChangeForm(self.request.user)
        context = {'form': form}
        return context

    def post(self, request, **kwargs):
        user = self.get_object()
        form = PasswordChangeForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            # Make sure user stays logged in
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password successfully changed")
            return redirect('home')
        else:
            return redirect('update_password')


class UpdateProfile(LoginRequiredMixin, UpdateView):
    template_name = 'users/update_profile.html'
    model = BaseUser
    form_class = UserUpdateForm

    def get_object(self):
        user = self.request.user
        return user

    def get_context_data(self, **kwargs):
        user_form = UserUpdateForm(instance=self.request.user)
        profile_form = ProfileUpdateForm(
            instance=self.request.user.user_profile)
        context = super(UpdateProfile, self).get_context_data(**kwargs)
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.user_profile)
        print(user.user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('update_profile')


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        profile = user.user_profile
        workouts = Workout.objects.filter(user=user)
        context = {
            'user': user,
            'profile': profile,
            'workouts': workouts
        }
        return context


class TempHome(TemplateView):
    template_name = 'users/home.html'


class Login(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('home')


class Registration(CreateView):
    template_name = 'users/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')


class Logout(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/', *args, **kwargs)
