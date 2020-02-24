from django.urls import path
from .views import yelpapi

urlpatterns = [
    path('index', yelpapi.IndexView.as_view(), name="yelpapi")
]