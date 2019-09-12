from django.urls import path
from .views import UserCreateView, UserLoginView


urlpatterns = [
    path('registration', UserCreateView.as_view()),
    path('authorization', UserLoginView.as_view()),
]
