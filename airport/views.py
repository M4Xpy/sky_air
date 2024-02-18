from rest_framework import viewsets, permissions

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer,
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


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination", )
    serializer_class = RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = permissions.IsAdminUser,
