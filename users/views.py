from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from users.forms import LoginUserForm, RegisterFormUser


# Клас для обробки логіну користувача з використанням форми LoginUserForm.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}

    def get_success_url(self):
        return reverse_lazy('home')


# Функція для виходу користувача з системи та перенаправлення на головну сторінку.
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


# Функція для реєстрації нового користувача та автоматичного логіну після успішної реєстрації.
def register(request):
    if request.method == "POST":
        form = RegisterFormUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return render(request, 'index.html')
    else:
        form = RegisterFormUser()
    return render(request, 'users/register.html', {'form': form})