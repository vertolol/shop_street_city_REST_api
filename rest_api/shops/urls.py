from django.urls import path
from .views import ShopListCreateView, ShopDetailView, StreetView, CityView


urlpatterns = [
    path('shop', ShopListCreateView.as_view()),
    path('shop/detail/<int:pk>', ShopDetailView.as_view()),
    path('<int:city_id>/street', StreetView.as_view()),
    path('city', CityView.as_view()),
]
