from rest_framework import serializers
from .models import Shop, Street, City


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ('id', 'name', 'city_name', 'city', 'street_name', 'street', 'house', 'opening_time', 'closing_time')
        extra_kwargs = {
            'city': {'write_only': True},
            'street': {'write_only': True},
        }


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ('id', 'name', 'city')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')
