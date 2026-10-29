from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import LoginUserForm


def login_user(request):
    if request.method == 'POST':#проверка коректности заполнения формы
        form = LoginUserForm(request.POST)
        if form.is_valid():    #для проверки заполнения полей
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)#Login фукн выполн тут авторизацию
                return HttpResponseRedirect(reverse('home'))

    else:
        form = LoginUserForm()

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))