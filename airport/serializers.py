from rest_framework import serializers

from airport.models import (
    Country,
    City, Airport,
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
            "country": {"write_only": True}
        }


class AirportSerializer(serializers.ModelSerializer):
    City = serializers.CharField(
        source="city.name", read_only=True, )

    class Meta:
        model = Airport
        fields = "id", "name", "City", "city",
        extra_kwargs = {
            "city": {"write_only": True}
        }
