import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def image_file_path(instance: any,
                    filename: str,
                    ) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join(f"uploads/{instance.__class__.__name__.lower()}/",
                        filename, )


class Country(models.Model):
    name = models.CharField(
        max_length=63, unique=True, )
    flag = models.ImageField(
        null=True, upload_to=image_file_path, )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "countries"
        ordering = ["name", ]


class City(models.Model):
    name = models.CharField(
        max_length=63, )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities", )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "cities"


class Airport(models.Model):
    name = models.CharField(
        max_length=63, )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="airports", )

    def __str__(self) -> str:
        return f"{self.name} - {self.city.name}"

    class Meta:
        unique_together = "name", "city",


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="source_routes", )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_routes", )
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

    def __str__(self) -> str:
        return f"{self.name} , {self.airline_type.name}"


class Crew(models.Model):
    first_name = models.CharField(max_length=63, )
    last_name = models.CharField(max_length=63, )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights", )
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights", )
    crew = models.ManyToManyField(
        Crew, related_name="flights", )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.route}/n{self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets", )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets", )
    row = models.IntegerField()
    seat = models.IntegerField()

    @staticmethod
    def validate_ticket(row: int,
                        seat: int,
                        airplane: Airplane,
                        error_to_raise: type[Exception],
                        ) -> None:
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {airplane_attr_name}): "
                                          f"(1, {count_attrs})"
                    }
                )

    def clean(self) -> None:
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def save(self,
             force_insert: bool = False,
             force_update: bool = False,
             using: str | None = None,
             update_fields: tuple[str] | None = None,
             ) -> None:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"{str(self.flight)} " \
               f"(row: {self.row}, seat: {self.seat})"

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]
