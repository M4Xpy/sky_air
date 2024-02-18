from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
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
    FlightSerializer,
    OrderSerializer,
    OrderListSerializer,
)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="country",
            type=str,
            description="Filter by country (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,

    def get_queryset(self):
        country = self.request.query_params.get("country")
        queryset = self.queryset

        if country:
            queryset = queryset.filter(
                name__icontains=country, )

        return queryset.distinct()


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="country",
            type=str,
            description="Filter by country (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,

    def get_queryset(self):
        country = self.request.query_params.get("country")
        queryset = self.queryset

        if country:
            queryset = queryset.filter(
                country__name__icontains=country, )

        return queryset.distinct()


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="city",
            type=str,
            description="Filter by city (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("city")
    serializer_class = AirportSerializer

    def get_queryset(self):
        city = self.request.query_params.get("city")
        queryset = self.queryset

        if city:
            queryset = queryset.filter(
                city__name__icontains=city, )

        return queryset.distinct()


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="source",
            type=str,
            description="Filter by source (case-insensitive)",
            required=False,
            location="query",
        ),
        OpenApiParameter(
            name="destinations",
            type=str,
            description="Filter by destination IDs (comma-separated)",
            required=False,
            location="query",
        ),
    ]
)
class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Route.objects.select_related("source", "destination", )
    serializer_class = RouteSerializer

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        queryset = self.queryset

        if source:
            queryset = queryset.filter(
                source__city__name__icontains=source, )
        if destination:
            queryset = queryset.filter(
                destination__city__name__icontains=destination, )

        return queryset.distinct()


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="type",
            type=str,
            description="Filter by type (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,

    def get_queryset(self):
        type = self.request.query_params.get("type")
        queryset = self.queryset

        if type:
            queryset = queryset.filter(
                name__icontains=type, )

        return queryset.distinct()


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="name",
            type=str,
            description="Filter by name (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(
                name__icontains=name, )

        return queryset.distinct()


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="full_name",
            type=str,
            description="Filter by full name (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = permissions.IsAdminUser,

    def get_queryset(self):
        full_name = self.request.query_params.get("full_name")
        queryset = self.queryset

        if full_name:
            queryset = queryset.filter(
                Q(first_name__icontains=full_name) | Q(last_name__icontains=full_name)
            )

        return queryset.distinct()


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.prefetch_related("route", "airplane", "crew")
    serializer_class = FlightSerializer
    permission_classes = IsAdminOrIfAuthenticatedReadOnly,


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="country",
            type=str,
            description="Filter by country (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route", "tickets__flight__airplane"
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
