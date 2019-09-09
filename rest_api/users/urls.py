from django.urls import path
from .views import UserCreateView, LoginView


urlpatterns = [
    path('registration', UserCreateView.as_view()),
    path('authorization', LoginView.as_view()),
]
