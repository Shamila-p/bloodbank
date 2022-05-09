from http.client import HTTPResponse
from re import A
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Donor
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.contrib import messages


def index(request):
    return redirect('/login')


@login_required
def home(request):
    donors = Donor.objects.all()
    return render(request, 'home.html', {'donors': donors})


@login_required
def add_donor(request):
    if request.method == "POST":
        name = request.POST["name"]
        place = request.POST["place"]
        blood_group = request.POST["blood_group"]
        phone = request.POST["phone"]
        donors = Donor.objects.create(
            name=name, place=place, bloodgroup=blood_group, phone=phone)
        donors.save()
        print('donor created')
        return redirect('/home')

    if request.method == "GET":
        return render(request, 'registration.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == "POST":
            name = request.POST["name"]
            username = request.POST["username"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            if name == "":
                messages.info(request, 'name field cannot be empty!!')
            elif username == "":
                messages.info(request, 'username field cannot be empty!!')
            elif password1 == "":
                messages.info(request, 'password field cannot be empty!!')
            elif password2 == "":
                messages.info(request, 'password field cannot be empty!!')
            else:
             if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'username taken')
                    return redirect('/signup')

                else:
                    user = User.objects.create_user(
                        username=username, first_name=name, password=password1)
                    user.save()
                    print('user created')
                    return redirect('/login')
             else:
                messages.info(request, 'password not matching')
            return redirect('/signup')

        else:
            return render(request, 'Signup.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            if username == "":
                messages.info(request, 'username field cannot be empty!!')
            elif password == "":
                messages.info(request, 'password field cannot be empty!!')
            else:
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                    auth.login(request, user)
                    return redirect_after_login(request)
                else:
                    messages.info(request, 'username/password incorrect!!')

            return redirect('/login')
        else:
            return render(request, 'login.html')


def redirect_after_login(request):
    nxt = request.POST.get("next", None)
    print(nxt)
    if nxt is None:
        return redirect(settings.LOGIN_REDIRECT_URL)
    elif not url_has_allowed_host_and_scheme(
            url=nxt,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()):
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(nxt)


def logout(request):
    auth.logout(request)
    return redirect('/login')
