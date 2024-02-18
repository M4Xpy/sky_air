from rest_framework import viewsets

from airport.models import (
    Country,
    City, Airport,
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (
    CountrySerializer,
    CitySerializer, AirportSerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("city")
    serializer_class = AirportSerializer

