from rest_framework import serializers

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane, Crew,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "id", "name", "flag",


class CitySerializer(serializers.ModelSerializer):
    Country = serializers.CharField(
        source="country.name", read_only=True, )

    class Meta:
        model = City
        fields = "id", "name", "country", "Country",
        extra_kwargs = {
            "country": {"write_only": True},
        }


class AirportSerializer(serializers.ModelSerializer):
    City = serializers.CharField(
        source="city.name", read_only=True, )

    class Meta:
        model = Airport
        fields = "id", "name", "City", "city",
        extra_kwargs = {
            "city": {"write_only": True},
        }


class RouteSerializer(serializers.ModelSerializer):
    Source = AirportSerializer(source="source", read_only=True, )
    Destination = AirportSerializer(source="destination", read_only=True, )

    class Meta:
        model = Route
        fields = "id", "Source", "Destination", "source", "destination", "distance",
        extra_kwargs = {
            "source": {"write_only": True},
            "destination": {"write_only": True},
        }


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "id", "name", "rows", "seats_in_row", "airline_type", "capacity",


class AirplaneShortSerializer(AirplaneSerializer):
    class Meta:
        model = Airplane
        fields = "name", "capacity",


class AirplaneTypeSerializer(serializers.ModelSerializer):
    airplanes = AirplaneShortSerializer(many=True, read_only=True)

    class Meta:
        model = AirplaneType
        fields = "name", "airplanes",


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "id", "first_name", "last_name",
