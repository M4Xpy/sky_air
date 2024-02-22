from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from airport.models import Country, City, Airport, Route


class CountryViewSetTestCase(APITestCase):
    def setUp(self):
        self.test_country = Country.objects.create(name="TestCountry")
        self.authenticated_user = get_user_model().objects.create_user(
            "test@authenticated.com",
            "authenticated_password",
        )
        self.client.force_authenticate(user=self.authenticated_user)
        self.response = self.client.get(
            reverse("airport:country-list"), {"country": "TestCountry"}
        )

        self.admin_user = get_user_model().objects.create_user(
            "test@admin.com",
            "admin_password",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.admin_user)
        self.user_response = self.client.get(
            reverse("airport:country-list"), {"country": "TestCountry"}
        )

    def test_admin_can_filter_countries_status(self):
        self.assertEqual(self.user_response.status_code, status.HTTP_200_OK)

    def test_admin_can_filter_countries_len(self):
        self.assertEqual(len(self.user_response.data), 1)

    def test_admin_can_filter_countries_name(self):
        self.assertEqual(self.user_response.data[0]["name"], "TestCountry")

    def test_authenticated_user_can_filter_countries_status(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_filter_countries_len(self):
        self.assertEqual(len(self.response.data), 1)

    def test_authenticated_user_can_filter_countries_name(self):
        self.assertEqual(self.response.data[0]["name"], "TestCountry")

    def test_non_authenticated_user_cant_filter_countries(self):
        self.client.logout()
        response = self.client.get(
            reverse("airport:country-list"), {"country": "TestCountry"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CityViewSetTestCase(APITestCase):
    def setUp(self):
        self.test_country = Country.objects.create(name="TestCountry")
        self.test_city = City.objects.create(name="TestCity", country=self.test_country)
        self.authenticated_user = get_user_model().objects.create_user(
            "test@authenticated.com",
            "authenticated_password",
        )
        self.client.force_authenticate(user=self.authenticated_user)
        self.response = self.client.get(
            reverse("airport:city-list"), {"city": "TestCity"}
        )

        self.admin_user = get_user_model().objects.create_user(
            "test@admin.com",
            "admin_password",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.admin_user)

        self.user_response = self.client.get(
            reverse("airport:city-list"), {"city": "TestCity"}
        )

    def test_admin_can_filter_cities_status(self):
        self.assertEqual(self.user_response.status_code, status.HTTP_200_OK)

    def test_admin_can_filter_cities_len(self):
        self.assertEqual(len(self.user_response.data), 1)

    def test_admin_can_filter_cities_name(self):
        self.assertEqual(self.user_response.data[0]["name"], "TestCity")

    def test_authenticated_user_can_filter_cities_status(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_filter_cities_len(self):
        self.assertEqual(len(self.response.data), 1)

    def test_authenticated_user_can_filter_cities_name(self):
        self.assertEqual(self.response.data[0]["name"], "TestCity")

    def test_non_authenticated_user_cant_filter_cities(self):
        self.client.logout()
        response = self.client.get(reverse("airport:city-list"), {"city": "TestCity"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AirportViewSetTestCase(APITestCase):
    def setUp(self):
        self.test_country = Country.objects.create(name="TestCountry")
        self.test_city = City.objects.create(name="TestCity", country=self.test_country)
        self.test_airport = Airport.objects.create(
            name="TestAirport", city=self.test_city
        )
        self.authenticated_user = get_user_model().objects.create_user(
            "test@authenticated.com",
            "authenticated_password",
        )
        self.client.force_authenticate(user=self.authenticated_user)
        self.response = self.client.get(
            reverse("airport:airport-list"), {"airport": "TestAirport"}
        )

        self.admin_user = get_user_model().objects.create_user(
            "test@admin.com",
            "admin_password",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.admin_user)
        #
        self.user_response = self.client.get(
            reverse("airport:airport-list"), {"airport": "TestAirport"}
        )

    def test_admin_can_filter_airports_status(self):
        self.assertEqual(self.user_response.status_code, status.HTTP_200_OK)

    def test_admin_can_filter_airports_len(self):
        self.assertEqual(len(self.user_response.data), 1)

    def test_admin_can_filter_airports_name(self):
        self.assertEqual(self.user_response.data[0]["name"], "TestAirport")

    def test_authenticated_user_can_filter_airports_status(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_filter_airports_len(self):
        self.assertEqual(len(self.response.data), 1)

    def test_authenticated_user_can_filter_airports_name(self):
        self.assertEqual(self.response.data[0]["name"], "TestAirport")

    def test_non_authenticated_user_can_filter_airports(self):
        self.client.logout()
        response = self.client.get(
            reverse("airport:airport-list"), {"airport": "TestAirport"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RouteViewSetTestCase(APITestCase):
    def setUp(self):
        self.test_country = Country.objects.create(name="TestCountry")
        self.test_city = City.objects.create(name="TestCity", country=self.test_country)
        self.test_airport = Airport.objects.create(
            name="TestAirport", city=self.test_city
        )
        self.test_route = Route.objects.create(
            source=self.test_airport, destination=self.test_airport
        )
        self.authenticated_user = get_user_model().objects.create_user(
            "test@authenticated.com",
            "authenticated_password",
        )
        self.client.force_authenticate(user=self.authenticated_user)
        self.response = self.client.get(
            reverse("airport:route-list"), {"routes": "TestRoute"}
        )

        self.admin_user = get_user_model().objects.create_user(
            "test@admin.com",
            "admin_password",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.admin_user)
        #
        self.user_response = self.client.get(
            reverse("airport:route-list"), {"route": "TestRoute"}
        )

    def test_admin_can_filter_routes_status(self):
        self.assertEqual(self.user_response.status_code, status.HTTP_200_OK)

    def test_admin_can_filter_routes_len(self):
        self.assertEqual(len(self.user_response.data), 1)

    def test_authenticated_user_can_filter_routes_status(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_filter_routes_len(self):
        self.assertEqual(len(self.response.data), 1)

    def test_non_authenticated_user_can_filter_routes(self):
        self.client.logout()
        response = self.client.get(
            reverse("airport:route-list"), {"route": "TestRoute"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
