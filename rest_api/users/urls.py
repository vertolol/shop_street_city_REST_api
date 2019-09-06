from django.urls import path
from .views import UserCreateView, login


urlpatterns = [
    path('registration', UserCreateView.as_view()),
    path('authorization', login),
]
