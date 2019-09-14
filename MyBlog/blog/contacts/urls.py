from django.conf.urls import url

from . import views

app_name = 'contacts'
urlpatterns = [
    url(r'^contact.*?/$', views.contact, name='contact'),
]