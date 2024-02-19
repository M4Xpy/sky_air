from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Ticket,
    Order,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "flag",
        )


class CitySerializer(serializers.ModelSerializer):
    Country = serializers.CharField(
        source="country.name",
        read_only=True,
    )

    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "country",
            "Country",
        )
        extra_kwargs = {
            "country": {"write_only": True},
        }


class AirportSerializer(serializers.ModelSerializer):
    City = serializers.CharField(
        source="city.name",
        read_only=True,
    )

    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "City",
            "city",
        )
        extra_kwargs = {
            "city": {"write_only": True},
        }


class AirportShortSerializer(AirportSerializer):
    class Meta:
        model = Airport
        fields = (
            "name",
            "City",
        )


class RouteSerializer(serializers.ModelSerializer):
    Source = AirportShortSerializer(
        source="source",
        read_only=True,
    )
    Destination = AirportShortSerializer(
        source="destination",
        read_only=True,
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "Source",
            "Destination",
            "source",
            "destination",
            "distance",
        )
        extra_kwargs = {
            "source": {"write_only": True},
            "destination": {"write_only": True},
        }


class RouteShortSerializer(RouteSerializer):
    class Meta:
        model = Route
        fields = (
            "Source",
            "Destination",
            "distance",
        )


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airline_type",
            "capacity",
        )


class AirplaneShortSerializer(AirplaneSerializer):
    class Meta:
        model = Airplane
        fields = (
            "name",
            "capacity",
        )


class AirplaneTypeSerializer(serializers.ModelSerializer):
    airplanes = AirplaneShortSerializer(many=True, read_only=True)

    class Meta:
        model = AirplaneType
        fields = (
            "name",
            "airplanes",
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class FlightSerializer(serializers.ModelSerializer):
    Route = RouteShortSerializer(
        source="route",
        read_only=True,
    )
    Airplane = AirplaneShortSerializer(
        source="airplane",
        read_only=True,
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "Route",
            "Airplane",
            "airplane",
            "crew",
            "departure_time",
            "arrival_time",
        )
        extra_kwargs = {
            "route": {"write_only": True},
            "airplane": {"write_only": True},
            "crew": {"write_only": True},
        }


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketListSerializer(TicketSerializer):
    movie_session = FlightSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
