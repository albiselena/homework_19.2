from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
import secrets
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegisterForm, UserUpdateForm
from .models import User
from django.urls import reverse

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    """Создание нового пользователя."""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Отправка письма с подтверждением
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)  # Генерация токена
        user.token = token  # Сохранение токена
        user.save()  # Сохранение пользователя
        host = self.request.get_host()  # Получение хоста
        url = f'http://{host}/users/email-confirm/{token}'  # Формирование ссылки которая будет отправлена на почту
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )  # Отправка письма
        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждение почты."""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class NewPasswordView(PasswordResetView):
    """Смена пароля."""
    form_class = PasswordResetForm
    template_name = 'users/password_reset_form.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)

        if user:
            password = User.objects.make_random_password(8)
            user.set_password(password)
            user.save()
            send_mail(
                subject='Новый пароль',
                message=f'Ваш новый новый пароль: {password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )
        return redirect(reverse('users:login'))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление данных пользователя."""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('catalog:products')
    login_url = reverse_lazy('users:login')

    def get_object(self):
        return self.request.user
