from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import UserRegisterForm
from .models import User


class UserCreateView(CreateView):
    """Создание нового пользователя."""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
