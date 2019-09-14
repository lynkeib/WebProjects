from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
import hashlib


# Create your views here.
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def login(request):
    message = ""
    if request.session.get('is_login', None):
        return render(request, "login.html", context={"logged_in": True})
    if request.method == "POST":
        username = request.POST['logname']
        password = request.POST['logpass']
        try:
            user = User.objects.get(username=username)
        except:
            message = "User doesn't exit"
            return render(request, 'login.html', context={'message': message})

        if user.password == hash_code(password):
            request.session["is_login"] = True
            request.session["user_id"] = user.pk
            request.session["user_name"] = user.username
            return render(request, "login.html", context={"logged_in": True})
        else:
            message = "Password is not correct"
            return render(request, 'login.html', context={"message": message})
    else:
        return render(request, "login.html", context={"message": message})


def signup(request):
    message = ""
    if request.method == 'POST':
        username = request.POST['logname']
        password = request.POST['logpass']
        repassword = request.POST['logrepass']
        if password != repassword or password == "":
            message = "Wrong Password (Blank is invaild), Please try again"
            return render(request, "signup.html", context={"message": message})
        else:
            sameuser = User.objects.filter(username=username)
            if username == "":
                message = "Username cannot be blank"
                return render(request, "signup.html", context={"message": message})
            if sameuser:
                message = "User already exits, please change another username"
                return render(request, "signup.html", context={"message": message})
            else:
                user = User()
                user.username = username
                user.password = hash_code(password)
                user.save()
                message = "Sign up success"
                return render(request, "signup.html", context={"message": message})
    return render(request, "signup.html", context={'message': message})


def signout(request):
    request.session.clear()
    return render(request, "login.html", context={'message': None})
