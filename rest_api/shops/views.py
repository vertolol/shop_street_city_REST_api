from datetime import datetime
from django.db.models import Q, F

from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from .serializers import ShopSerializer, StreetSerializer, CitySerializer
from .models import Shop, Street, City
from .config import STREET, CITY, STATE_SHOP, SHOP_OPEN, SHOP_CLOSED


def get_queryset_from_working_hours(state_shop, queryset):
    now = datetime.now().time()

    if state_shop == SHOP_OPEN:
        closes_before_midnight = queryset.filter(Q(opening_time__lt=F('closing_time')),
                                                 Q(opening_time__lte=now), Q(closing_time__gt=now))
        closes_after_midnight = queryset.filter(Q(opening_time__gte=F('closing_time')),
                                                Q(opening_time__lte=now) | Q(closing_time__gt=now))
        queryset = closes_before_midnight | closes_after_midnight

    elif state_shop == SHOP_CLOSED:
        closes_before_midnight = queryset.filter(Q(opening_time__lt=F('closing_time')),
                                                 Q(opening_time__lt=now), Q(closing_time__lte=now))
        closes_after_midnight = queryset.filter(Q(opening_time__gte=F('closing_time')),
                                                Q(opening_time__gt=now) | Q(closing_time__lte=now))
        queryset = closes_before_midnight | closes_after_midnight

    return queryset


class ShopView(ListCreateAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        queryset = Shop.objects.all()
        street = self.request.query_params.get(STREET, None)
        city = self.request.query_params.get(CITY, None)
        state_shop = self.request.query_params.get(STATE_SHOP, None)

        if city:
            queryset = queryset.filter(city=city)

        if street:
            if city is not None:
                queryset = queryset.filter(street=street)
            else:
                raise ParseError({'Description': 'city field required when passing street field'})

        if state_shop:
            queryset = get_queryset_from_working_hours(state_shop, queryset)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'Message': f'You have successfully register shop, ID: {serializer.data["id"]}'})


class StreetView(ListAPIView):
    serializer_class = StreetSerializer

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return Street.objects.filter(city=city_id)


class CityView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
