from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from airport.models import (
    City,
    Airport,
    Country,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
)


class ModelsTests(TestCase):
    def setUp(self):
        self.england = Country.objects.create(name="England")
        self.london = City.objects.create(name="London", country=self.england)
        self.london_airport = Airport.objects.create(
            name="Heathrow (LHR)",
            city=self.london,
        )
        self.route_zero = Route.objects.create(
            source=self.london_airport,
            destination=self.london_airport,
        )
        self.route_222 = Route.objects.create(
            source=self.london_airport,
            destination=self.london_airport,
            distance=222,
        )
        self.test_type = AirplaneType.objects.create(
            name="testType",
        )
        self.test_airplane = Airplane.objects.create(
            name="testAirplane",
            rows=2,
            seats_in_row=3,
            airline_type_id=self.test_type.id,
        )
        self.test_crew = Crew.objects.create(
            first_name="Test",
            last_name="Crew",
        )
        self.test_flight = Flight.objects.create(
            route=self.route_zero,
            airplane=self.test_airplane,
            departure_time="2021-02-01",
            arrival_time="2021-02-01",
        )
        self.test_user = get_user_model().objects.create_user(
            email="test@test.com", password="test_password"
        )
        self.first_order = Order.objects.create(
            created_at="2021-01-01",
            user=self.test_user,
        )
        self.second_order = Order.objects.create(
            created_at="2022-02-02",
            user=self.test_user,
        )
        self.test_ticket = Ticket(
            flight=self.test_flight,
            order=self.first_order,
            row=2,
            seat=3,
        )

    def test_country_creation(self):
        """Test the creation of a new country"""
        self.assertEqual(self.england.name, "England")

    def test_empty_flag(self):
        self.assertEqual(bool(self.england.flag), False)

    def test_country_str_method(self):
        """Test the __str__ method of the Country model"""
        self.assertEqual(str(self.england), "England")

    def test_city_creation(self):
        """Test the creation of a new city"""
        self.assertEqual(self.london.name, "London")

    def test_city_in_country(self):
        """Test if the city belongs to the correct country"""
        self.assertEqual(self.london.country, self.england)

    def test_city_str_method(self):
        """Test the __str__ method of the City model"""
        self.assertEqual(str(self.london), "London")

    def test_airport_str(self):
        self.assertEqual(
            str(self.london_airport),
            f"{self.london_airport.name} - {self.london_airport.city.name}",
        )

    def test_airport_creation(self):
        """Test the creation of a new airport"""
        self.assertEqual(self.london_airport.name, "Heathrow (LHR)")

    def test_airport_city_relationship(self):
        """Test if the airport's city matches the expected city."""
        self.assertEqual(self.london_airport.city, self.london)

    def test_airport_str_method(self):
        """Test the __str__ method of the Airport model"""
        self.assertEqual(str(self.london_airport), "Heathrow (LHR) - London")

    # def test_airport_uniqueness_within_city(self):
    #     """Test uniqueness of airport names within a city"""
    #     # # Try creating another airport with the same name in the same city
    #     Airport.objects.create(name="TestAirport", city=self.test_city)
    #     Airport.objects.create(name="TestAirport", city=self.test_city)
    #     Airport.objects.create(name="TestAirport", city=self.test_city)
    #     x = Airport.objects.filter(name="TestAirport", city=self.test_city).count()
    #     Airport.objects.create(name="TestAirport", city=self.test_city)
    #     self.assertEqual(x, Airport.objects.filter(name="TestAirport", city=self.test_city).count())

    def test_both_routes_creation(self):
        """Test the creation of the both routes"""
        self.assertEqual(Route.objects.count(), 2)

    def test_route_zero(self):
        """Test if calculate_distance() method returns 0 for similar points"""
        self.assertEqual(self.route_zero.distance, 0)

    def test_route_one(self):
        """test of manual distance defining"""
        self.assertEqual(self.route_222.distance, 222)

    def test_route_str(self):
        """Test if the string representation of a route is correct."""
        self.assertEqual(
            str(self.route_zero),
            f"{self.route_zero.source.city.name}, {self.route_zero.source.city.country.name}"
            f" - {self.route_zero.destination.city.name}, {self.route_zero.destination.city.country.name}",
        )

    def test_airplane_type_creation(self):
        """Test the creation of an airplane type"""
        self.assertEqual(self.test_type.name, "testType")

    def test_airplane_type_str_method(self):
        """Test the __str__ method of an airplane type"""
        self.assertEqual(str(self.test_type), "testType")

    def test_airplane_creation(self):
        """Test the creation of an airplane"""
        self.assertEqual(self.test_airplane.name, "testAirplane")

    def test_airplane_str(self):
        """Test the __str__ method of an airplane"""
        self.assertEqual(
            str(self.test_airplane),
            f"{self.test_airplane.name} , {self.test_airplane.airline_type.name}", )

    def test_airplane_capacity(self):
        """Test capacity property of an airplane"""
        self.assertEqual(self.test_airplane.capacity, 6)

    def test_crew_str_and_full_name(self):
        """Test the __str__ equal to full_name property"""
        self.assertEqual(str(self.test_crew), self.test_crew.full_name)

    def test_flight_str(self):
        self.assertEqual(
            str(self.test_flight),
            f"{self.test_flight.route}/n{self.test_flight.departure_time}",
        )

    def test_order_str_method(self):
        """Test the __str__ method of the Order model."""
        self.assertEqual(
            str(self.first_order),
            str(self.first_order.created_at),
        )

    def test_order_ordering(self):
        """Test the ordering of orders by 'created_at'."""
        orders = Order.objects.all()
        self.assertEqual(orders[1], self.first_order)
        self.assertEqual(orders[0], self.second_order)

    def test_validate_ticket_valid_values(self):
        """Test validate_ticket with valid row and seat numbers."""
        Ticket.validate_ticket(2, 3, self.test_airplane, ValidationError)

    def test_clean_method(self):
        """Test the clean method of the Ticket model."""
        self.test_ticket.clean()

    def test_ticket_str_method(self):
        """Test the __str__ method of the Ticket model."""
        self.assertEqual(
            str(self.test_ticket),
            f"{str(self.test_flight)} (row: 2, seat: 3)",
        )
