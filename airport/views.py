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
    RouteListSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    CrewSerializer,
    FlightSerializer,
    OrderSerializer,
    OrderListSerializer,
    FlightDetailSerializer,
    RouteDetailSerializer,
    CityListSerializer,
    CityDetailSerializer,
    AirportListSerializer,
    AirportDetailSerializer,
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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        country = self.request.query_params.get("country")
        queryset = self.queryset

        if country:
            queryset = queryset.filter(
                name__icontains=country,
            )

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
        OpenApiParameter(
            name="city",
            type=int,
            description="Filter by city name (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = CityListSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        country = self.request.query_params.get("country")
        city = self.request.query_params.get("city")

        if country:
            queryset = queryset.filter(
                country__name__icontains=country,
            )

        if city:
            queryset = queryset.filter(
                name__icontains=city,
            )

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return CityListSerializer
        return CityDetailSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="city",
            type=str,
            description="Filter by city (case-insensitive)",
            required=False,
            location="query",
        ),
        OpenApiParameter(
            name="airport",
            type=str,
            description="Filter by airport (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("city")

    def get_queryset(self):
        queryset = self.queryset
        city = self.request.query_params.get("city")
        airport = self.request.query_params.get("airport")

        if city:
            queryset = queryset.filter(
                city__name__icontains=city,
            )

        if airport:
            queryset = queryset.filter(name__icontains=airport)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        return AirportDetailSerializer


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
            name="destination",
            type=str,
            description="Filter by destination (case-insensitive)",
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
    queryset = Route.objects.select_related(
        "source__city",
        "destination__city",
    )

    def get_queryset(self):
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        queryset = self.queryset

        if source:
            queryset = queryset.filter(
                source__city__name__icontains=source,
            )
        if destination:
            queryset = queryset.filter(
                destination__city__name__icontains=destination,
            )

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return RouteDetailSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="airplane_type",
            type=str,
            description="Filter by airplane type (case-insensitive)",
            required=False,
            location="query",
        ),
    ]
)
class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.prefetch_related("airplanes")
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        airplane_type = self.request.query_params.get("airplane_type")
        queryset = self.queryset

        if airplane_type:
            queryset = queryset.filter(
                name__icontains=airplane_type,
            )

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
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(
                name__icontains=name,
            )

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
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        full_name = self.request.query_params.get("full_name")
        queryset = self.queryset

        if full_name:
            queryset = queryset.filter(
                Q(first_name__icontains=full_name) | Q(last_name__icontains=full_name)
            )

        return queryset.distinct()


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.prefetch_related(
        "route__source__city", "route__destination__city", "airplane", "crew"
    )
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        departure = self.request.query_params.get("departure")
        arrival = self.request.query_params.get("arrival")
        source = self.request.query_params.get("city")
        destination = self.request.query_params.get("destination")

        if departure:
            queryset = queryset.filter(departure_time__contains=departure)
        if arrival:
            queryset = queryset.filter(arrival_time__contains=arrival)
        if source:
            queryset = queryset.filter(route__source__name__icontains=source)
        if destination:
            queryset = queryset.filter(route__destination__name__icontains=destination)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightSerializer
        return FlightDetailSerializer


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
