from django.urls import path, include
from profile_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(prefix="hello-viewsset", viewset=views.HelloViewSet, basename="hello-viewset")
router.register(prefix="profile", viewset=views.UserProfileViewSet)
router.register(prefix="feed", viewset=views.UserProfileFeedViewSet)

urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
    path("login/", views.UserLoginApiView.as_view()),
    path("", include(router.urls)),
]
