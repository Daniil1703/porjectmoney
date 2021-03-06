from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractBaseUser
from .models import CustomUser
from .forms import CustomUserCreationForm, LoginForm, CaptchaForm, SecureLoginForm


class UserCreate(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(
            request, 'users/registration.html', context={'form': form}
        )

    def post(self, request):
        if request.method == 'POST':
            bound_form = CustomUserCreationForm(request.POST)
            if bound_form.is_valid():
                bound_form.save()
                messages.success(request, 'Аккаунт успешно создан!')
                return redirect('mainsite:dashboard')
        else:
            bound_form = CustomUserCreationForm()
        return render(
               request, 'users/registration.html', context={'form': bound_form}
               )

class UserLogin(View):

    def get(self, request):
        #если попыток входа не было вообще
        if 'try_login' not in request.session:
            #создаем ключ try_login со значением false
            request.session['try_login'] = False
            check_try_login = request.session['try_login']
            #обрабатываем форму без капчи
            form = LoginForm()
        #если попытка входа уже была
        else:
            #запоминаем значение в переменную
            check_try_login = request.session['try_login']
            if not check_try_login:
                # Если попытки входа не было, но сессия try_login есть,
                # то отображаем форму без капчи
                form = LoginForm()
            else:
                # Если попытка входа была, то отображаем форму с капчей
                form = SecureLoginForm()
                captcha_reload = True
        return render(
            request, 'users/login.html', context={'form': form}
        )

    def post(self, request):
        if request.method == 'POST':
            # запоминаем значение try_login в переменную
            check_try_login = request.session['try_login']
            if not check_try_login:
                # Если попытки входа не было, то проверяем и отправляем форму
                # в которой нет поля капчи
                bound_form = LoginForm(request.POST)
                if bound_form.is_valid():
                    cd = bound_form.cleaned_data
                    user = authenticate(
                        request, email=cd['email'], password=cd['password']
                    )
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        messages.success(request, 'Вы успешно вошли в систему!')
                        del request.session['try_login']
                        return redirect('mainsite:dashboard')
                    else:
                        return HttpResponse('Disabled account')
                else:
                    messages.error(
                        request, 'Неверный ввод данных'
                        )
                    request.session['try_login'] = True
                    return redirect('users:login')
            # Если попытка входа была, то проверяем и отправляем форму
            # в которой есть поле капчи
            else:
                bound_form = SecureLoginForm(request.POST)
                captcha_reload = True
                if bound_form.is_valid():
                    cd = bound_form.cleaned_data
                    user = authenticate(
                        request, email=cd['email'], password=cd['password']
                    )
                else:
                    # если введеная капча не проходит проверку, то
                    # сбрасываем все введенные данные и вызываем ошибку
                    messages.error(
                        request, 'Неверный ввод данных'
                        )
                    return redirect('users:login')
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        messages.success(
                            request,
                            'Вы успешно вошли в систему!'
                        )
                        del request.session['try_login']
                        return redirect('mainsite:dashboard')
                    else:
                        return HttpResponse('Disabled account')
                else:
                    messages.error(
                        request, 'Неверный ввод данных'
                        )
                    # Если введенные данные пользователя не проходят проверку,
                    # то запоминаем попытку входа, и сбрасываем все введенные
                    # данные
                    request.session['try_login'] = True
                    return redirect('users:login')
        else:
            bound_form = SecureLoginForm()
        return render(
               request, 'users/login.html', context={
                    'form': bound_form,
                    }
               )

def message_change_password(request):
    messages.success(request, 'Вы успешно сменили пароль!')
    return redirect('mainsite:dashboard')

def logout_view(request):
    logout(request)
    messages.warning(request, 'Вы вышли из системы!')
    return redirect('users:login')
