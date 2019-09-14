from django.conf.urls import url, re_path

from . import views

app_name = 'user'
urlpatterns = [
    re_path(r'^login.*?/$', views.login, name='login'),
    re_path(r"^signup.*?/$", views.signup, name='signup'),
    re_path(r"^singout.*?/$", views.signout, name='signout')
]
