import os
import uuid
import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db import models
from django.utils.text import slugify
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def image_file_path(instance: any,
                    filename: str,
                    ) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join(f"uploads/{instance.__class__.__name__.lower()}/",
                        filename, )


class Country(models.Model):
    name = models.CharField(
        max_length=63, unique=True, )
    flag = models.ImageField(
        null=True, upload_to=image_file_path, )

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(
        max_length=63, )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities", )

    def __str__(self) -> str:
        return self.name


class Airport(models.Model):
    name = models.CharField(
        max_length=63, )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="airports", )

    def __str__(self) -> str:
        return f"{self.name} - {self.city.name}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="routes", )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="routes", )
    distance = models.IntegerField(
        default=0, )

    def calculate_distance(self) -> int:
        geolocator = Nominatim(user_agent="distance_calculator")

        location1 = geolocator.geocode(
            f"{self.source.city.name}, {self.source.city.country.name}")
        location2 = geolocator.geocode(
            f"{self.destination.city.name}, {self.destination.city.country.name}")

        # Calculate the distance between the two coordinates
        distance = geodesic((location1.latitude, location1.longitude),
                            (location2.latitude, location2.longitude)).kilometers
        return int(distance)

    def save(self, *args: any, **kwargs: any) -> None:
        if not self.distance:
            self.distance = self.calculate_distance()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (f"{self.source.city.name}, {self.source.city.country.name}"
                f" - {self.destination.city.name}, {self.destination.city.country.name}")


class AirplaneType(models.Model):
    name = models.CharField(
        max_length=63, unique=True, )

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    name = models.CharField(
        max_length=63, unique=True, )
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airline_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes", )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} , {self.airline_type.name}"
