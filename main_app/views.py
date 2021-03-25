import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

from .models import *
DAYS_FOR_13_YEARS = 4749
# SECONDS_FOR_13_YEARS = 410248800

def index(request):
	return render(request, 'index.html')

def register(request):
    print(request.POST)
    errors = User.objects.validation_register(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect("/")

    else:
        donut = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            birth_date = request.POST['birth_date'],
            email = request.POST["email"],
            password = donut
        )
        request.session['uuid'] = user.id
    return redirect('/success')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect("/")
    else:
        user_list = User.objects.filter(email = request.POST['email'])
        user = user_list[0]
        request.session['uuid'] = user.id
        return redirect('/success')

def logout(request):
    del request.session['uuid']
    return redirect("/")


def success(request):
    context = {
        'user': User.objects.get(id = request.session['uuid'])
    }
    return render(request, "success.html", context)