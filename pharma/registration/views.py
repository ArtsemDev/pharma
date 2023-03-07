from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegisterForm, LoginForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('signin')


class SignInView(LoginView):
    form_class = LoginForm
