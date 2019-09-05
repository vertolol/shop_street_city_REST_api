from django.urls import path
from .views import ShopView, StreetView, CityView


urlpatterns = [
    path('shop', ShopView.as_view()),
    path('<int:city_id>/street', StreetView.as_view()),
    path('city', CityView.as_view()),
]
