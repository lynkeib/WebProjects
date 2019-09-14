from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
import hashlib
import datetime
from . import models
from django.conf import settings
import pytz


# Create your views here.
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    from uuid import uuid4
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = str(uuid4())
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = 'Confirmation Email'

    text_content = '''Welcome'''

    html_content = '''
                        <p>Thank you for the registration<a href="http://{}/confirmation/?code={}" target=blank> www.1117.link </a>，\
                        </p>
                        <p>Please click the link to finish the registration</p>
                        <p>The vaild days for this link is {} days！</p>
                        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")

    msg.send()


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

        if user.password == hash_code(password) and user.has_confirmed == True:
            request.session["is_login"] = True
            request.session["user_id"] = user.pk
            request.session["user_name"] = user.username
            return render(request, "login.html", context={"logged_in": True})
        else:
            message = "Password is not correct (Or you haven't confirm your email)"
            return render(request, 'login.html', context={"message": message})
    else:
        return render(request, "login.html", context={"message": message})


def signup(request):
    message = ""
    if request.method == 'POST':
        username = request.POST['logname']
        email = request.POST['email']
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

                sameemail = User.objects.filter(email=email)
                if sameemail:
                    message = "This email already exits, please try another email"
                    return render(request, "signup.html", context={"message": message})
                else:
                    user = User()
                    user.username = username
                    user.password = hash_code(password)
                    user.email = email
                    user.save()
                    code = make_confirm_string(user)
                    send_email(email, code)

                    message = "Email is sent, please check your mail box"
                    confirm = True
                    return render(request, "confirmation.html", context=locals())
    return render(request, "signup.html", context={'message': message})


def signout(request):
    request.session.clear()
    return render(request, "login.html", context={'message': None})


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = 'Confirmation Invalid'
        confirm = False
        return render(request, 'confirmation.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('UTC'))

    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = 'Your email is expire, please sign up again'
        confirm = False
        return render(request, 'confirmation.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = 'You have been successfully signed up, try log in'
        return render(request, 'confirmation.html', locals())
