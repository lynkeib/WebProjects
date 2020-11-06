from django.urls import path, include
from profile_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(prefix="hello-viewsset", viewset=views.HelloViewSet, basename="hello-viewset")

urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
    path("", include(router.urls))
]
