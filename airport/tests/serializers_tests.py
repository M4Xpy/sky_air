from django.test import TestCase

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    Airplane,
    AirplaneType,
    Crew,
)
from airport.serializers import (
    CountrySerializer,
    CityListSerializer,
    AirportListSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneSerializer,
    AirplaneShortSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
)


class CountrySerializerTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country", flag="test_flag.png")
        self.serializer = CountrySerializer(instance=self.country)
        self.data = self.serializer.data

    def test_serializer_includes_id_field(self):
        """Test if the serializer includes the 'id' field."""
        self.assertIn("id", self.data)

    def test_serializer_includes_name_field(self):
        """Test if the serializer includes the 'name' field."""
        self.assertIn("name", self.data)

    def test_serializer_includes_flag_field(self):
        """Test if the serializer includes the 'flag' field."""
        self.assertIn("flag", self.data)

    def test_serializer_id_matches_instance_id(self):
        """Test if the serialized 'id' matches the instance ID."""
        self.assertEqual(self.data["id"], self.country.id)

    def test_serializer_name_matches_instance_name(self):
        """Test if the serialized 'name' matches the instance name."""
        self.assertEqual(self.data["name"], self.country.name)


class CitySerializerTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country")
        self.city = City.objects.create(name="Test City", country=self.country)
        self.serializer = CityListSerializer(instance=self.city)
        self.data = self.serializer.data

    def test_serializer_includes_id_field(self):
        """Test if the serializer includes the 'id' field."""
        self.assertIn("id", self.data)

    def test_serializer_includes_name_field(self):
        """Test if the serializer includes the 'name' field."""
        self.assertIn("name", self.data)

    def test_serializer_includes_Country_field(self):
        """Test if the serializer includes the 'Country' field."""
        self.assertIn("country", self.data)

    def test_serializer_id_matches_instance_id(self):
        """Test if the serialized 'id' matches the instance ID."""
        self.assertEqual(self.data["id"], self.city.id)

    def test_serializer_name_matches_instance_name(self):
        """Test if the serialized 'name' matches the instance name."""
        self.assertEqual(self.data["name"], self.city.name)

    def test_serializer_Country_matches_instance_country_name(self):
        """Test if the serialized 'Country' matches the instance country name."""
        self.assertEqual(self.data["country"], self.country.name)


class AirportSerializersTests(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test Country")
        self.city = City.objects.create(name="Test City", country=self.country)
        self.airport = Airport.objects.create(name="Test Airport", city=self.city)
        self.serializer = AirportListSerializer(instance=self.airport)
        self.data = self.serializer.data


class AirportListSerializerTestCase(AirportSerializersTests):
    def test_serializer_includes_id_field(self):
        """Test if the serializer includes the 'id' field."""
        self.assertIn("id", self.data)

    def test_serializer_includes_name_field(self):
        """Test if the serializer includes the 'name' field."""
        self.assertIn("name", self.data)

    def test_serializer_includes_City_field(self):
        """Test if the serializer includes the 'City' field."""
        self.assertIn("city", self.data)

    def test_serializer_id_matches_instance_id(self):
        """Test if the serialized 'id' matches the instance ID."""
        self.assertEqual(self.data["id"], self.airport.id)

    def test_serializer_name_matches_instance_name(self):
        """Test if the serialized 'name' matches the instance name."""
        self.assertEqual(self.data["name"], self.airport.name)

    def test_serializer_City_matches_instance_city_name(self):
        """Test if the serialized 'City' matches the instance city name."""
        self.assertEqual(self.data["city"], self.city.name)


# class AirportShortSerializerTestCase(AirportSerializersTests):
#     def test_airport_short_serializer_includes_name_field(self):
#         """Test if the airport short serializer includes the 'name' field."""
#         self.assertIn("name", self.data)
#
#     def test_airport_short_serializer_includes_City_field(self):
#         """Test if the airport short serializer includes the 'City' field."""
#         self.assertIn("city", self.data)
#
#     def test_airport_short_serializer_name_matches_instance_name(self):
#         """Test if the serialized 'name' matches the instance name."""
#         self.assertEqual(self.data["name"], self.airport.name)
#
#     def test_airport_short_serializer_City_matches_instance_city_name(self):
#         """Test if the serialized 'City' matches the instance city name."""
#         self.assertEqual(self.data["city"], self.city.name)


class RouteSerializersTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Test country")
        self.city = City.objects.create(name="London", country=self.country)
        self.source_airport = Airport.objects.create(
            name="Source Airport", city=self.city
        )
        self.destination_airport = Airport.objects.create(
            name="Destination Airport", city=self.city
        )
        self.route = Route.objects.create(
            source=self.source_airport,
            destination=self.destination_airport,
            distance=100,
        )
        self.serializer = RouteListSerializer(instance=self.route)
        self.data = self.serializer.data
        self.short_serializer = RouteDetailSerializer(instance=self.route)
        self.short_data = self.short_serializer.data


class RouteSerializerTestCase(RouteSerializersTest):
    def test_route_serializer_includes_id_field(self):
        """Test if the route serializer includes the 'id' field."""
        self.assertIn("id", self.data)

    def test_route_serializer_includes_Source_field(self):
        """Test if the route serializer includes the 'Source' field."""
        self.assertIn("source", self.data)

    def test_route_serializer_includes_Destination_field(self):
        """Test if the route serializer includes the 'Destination' field."""
        self.assertIn("destination", self.data)

    def test_route_serializer_includes_distance_field(self):
        """Test if the route serializer includes the 'distance' field."""
        self.assertIn("distance", self.data)

    def test_route_serializer_id_matches_instance_id(self):
        """Test if the serialized 'id' matches the instance ID."""
        self.assertEqual(self.data["id"], self.route.id)

    def test_route_serializer_source_matches_instance_source_name(self):
        """Test if the serialized 'source' matches the instance source name."""
        self.assertEqual(self.data["source"]["name"], self.source_airport.name)

    def test_route_serializer_distance_matches_instance_distance(self):
        """Test if the serialized 'distance' matches the instance distance."""
        self.assertEqual(self.data["distance"], self.route.distance)

    def test_route_serializer_destination_matches_instance_destination_name(self):
        """Test if the serialized 'destination' matches the instance destination name."""
        self.assertEqual(
            self.data["destination"]["name"], self.destination_airport.name
        )


class RouteShortSerializerTestCase(RouteSerializersTest):
    def test_route_short_serializer_includes_Source_field(self):
        """Test if the route short serializer includes the 'Source' field."""
        self.assertIn("source", self.short_data)

    def test_route_short_serializer_includes_Destination_field(self):
        """Test if the route short serializer includes the 'Destination' field."""
        self.assertIn("destination", self.short_data)

    def test_route_short_serializer_includes_distance_field(self):
        """Test if the route short serializer includes the 'distance' field."""
        self.assertIn("distance", self.short_data)

    def test_route_short_serializer_source_matches_instance_source_name(self):
        """Test if the serialized 'Source' matches the instance source name."""
        self.assertEqual(self.short_data["source"], self.source_airport.id)

    def test_route_short_serializer_destination_matches_instance_destination_name(self):
        """Test if the serialized 'Destination' matches the instance destination name."""
        self.assertEqual(self.short_data["destination"], self.destination_airport.id)

    def test_route_short_serializer_distance_matches_instance_distance(self):
        """Test if the serialized 'distance' matches the instance distance."""
        self.assertEqual(self.short_data["distance"], self.route.distance)


class AirplaneSerializersTestCase(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="TestType")
        self.airplane = Airplane.objects.create(
            name="Test Airplane",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )
        self.serializer = AirplaneSerializer(instance=self.airplane)
        self.data = self.serializer.data
        self.short_serializer = AirplaneShortSerializer(instance=self.airplane)
        self.short_data = self.short_serializer.data

    def test_airplane_serializer_includes_id_field(self):
        """Test if the airplane serializer includes the 'id' field."""
        self.assertIn("id", self.data)

    def test_airplane_serializer_includes_name_field(self):
        """Test if the airplane serializer includes the 'name' field."""
        self.assertIn("name", self.data)

    def test_airplane_serializer_includes_rows_field(self):
        """Test if the airplane serializer includes the 'rows' field."""
        self.assertIn("rows", self.data)

    def test_airplane_serializer_includes_seats_in_row_field(self):
        """Test if the airplane serializer includes the 'seats_in_row' field."""
        self.assertIn("seats_in_row", self.data)

    def test_airplane_serializer_includes_airplane_type_field(self):
        """Test if the airplane serializer includes the 'airplane_type' field."""
        self.assertIn("airplane_type", self.data)

    def test_airplane_serializer_includes_capacity_field(self):
        """Test if the airplane serializer includes the 'capacity' field."""
        self.assertIn("capacity", self.data)

    def test_airplane_short_serializer_includes_name_field(self):
        """Test if the airplane short serializer includes the 'name' field."""
        self.assertIn("name", self.short_data)

    def test_airplane_short_serializer_includes_capacity_field(self):
        """Test if the airplane short serializer includes the 'capacity' field."""
        self.assertIn("capacity", self.short_data)

    def test_airplane_serializer_id_matches_instance_id(self):
        """Test if the serialized 'id' matches the instance ID."""
        self.assertEqual(self.data["id"], self.airplane.id)

    def test_airplane_serializer_name_matches_instance_name(self):
        """Test if the serialized 'name' matches the instance name."""
        self.assertEqual(self.data["name"], self.airplane.name)

    def test_airplane_serializer_rows_matches_instance_rows(self):
        """Test if the serialized 'rows' matches the instance rows."""
        self.assertEqual(self.data["rows"], self.airplane.rows)

    def test_airplane_serializer_seats_in_row_matches_instance_seats_in_row(self):
        """Test if the serialized 'seats_in_row' matches the instance seats_in_row."""
        self.assertEqual(self.data["seats_in_row"], self.airplane.seats_in_row)

    def test_airplane_serializer_airplane_type_matches_instance_airplane_type(self):
        """Test if the serialized 'airplane_type' matches the instance airplane_type."""
        self.assertEqual(self.data["airplane_type"], self.airplane.airplane_type.id)

    def test_airplane_serializer_capacity_calculation(self):
        """Test if the capacity calculation is correct."""
        self.assertEqual(
            self.data["capacity"], self.airplane.rows * self.airplane.seats_in_row
        )


class AirplaneTypeSerializerTestCase(TestCase):
    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Test Airplane Type")
        self.airplane1 = Airplane.objects.create(
            name="Airplane 1", rows=10, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.airplane2 = Airplane.objects.create(
            name="Airplane 2", rows=8, seats_in_row=4, airplane_type=self.airplane_type
        )
        self.serializer = AirplaneTypeSerializer(instance=self.airplane_type)
        self.data = self.serializer.data

    def test_airplane_type_serializer_includes_name_field(self):
        """Test if the airplane type serializer includes the 'name' field."""
        self.assertIn("name", self.data)

    def test_airplane_type_serializer_includes_airplanes_field(self):
        """Test if the airplane type serializer includes the 'airplanes' field."""
        self.assertIn("airplanes", self.data)

    def test_airplane_type_serializer_name_matches_instance_name(self):
        """Test if the serialized 'name' matches the instance name."""
        self.assertEqual(self.data["name"], self.airplane_type.name)

    def test_airplane_type_serializer_airplanes_match_instance_airplanes(self):
        """Test if the serialized 'airplanes' match the instance airplanes."""
        self.assertEqual(
            [airplane["name"] for airplane in self.data["airplanes"]],
            [airplane.name for airplane in self.airplane_type.airplanes.all()],
        )


class CrewSerializerTestCase(TestCase):
    def setUp(self):
        self.crew_member = Crew.objects.create(first_name="John", last_name="Doe")

        self.serializer = CrewSerializer(instance=self.crew_member)
        self.data = self.serializer.data

    def test_crew_serializer_includes_id_field(self):
        """Test if the crew serializer includes the 'id' field."""
        self.assertIn("id", self.data)

    def test_crew_serializer_includes_first_name_field(self):
        """Test if the crew serializer includes the 'first_name' field."""
        self.assertIn("first_name", self.data)

    def test_crew_serializer_includes_last_name_field(self):
        """Test if the crew serializer includes the 'last_name' field."""
        self.assertIn("last_name", self.data)

    def test_crew_serializer_id_matches_instance_id(self):
        """Test if the serialized 'id' matches the instance ID."""
        self.assertEqual(self.data["id"], self.crew_member.id)

    def test_crew_serializer_first_name_matches_instance_first_name(self):
        """Test if the serialized 'first_name' matches the instance first name."""
        self.assertEqual(self.data["first_name"], self.crew_member.first_name)

    def test_crew_serializer_last_name_matches_instance_last_name(self):
        """Test if the serialized 'last_name' matches the instance last name."""
        self.assertEqual(self.data["last_name"], self.crew_member.last_name)
