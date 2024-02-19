from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from airport.models import Country


class CountryViewSetTestCase(APITestCase):
    def setUp(self):
        self.country1 = Country.objects.create(name="Test Country 1")
        self.authenticated_user = get_user_model().objects.create_user(
            "test@authenticated.com",
            "authenticated_password",
        )
        self.client.force_authenticate(user=self.authenticated_user)
        self.response = self.client.get(
            reverse("airport:country-list"), {"country": "Test Country 1"}
        )

        self.admin_user = get_user_model().objects.create_user(
            "test@admin.com",
            "admin_password",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.admin_user)
        self.user_response = self.client.get(
            reverse("airport:country-list"), {"country": "Test Country 1"}
        )

    def test_admin_can_filter_countries_status(self):
        self.assertEqual(self.user_response.status_code, status.HTTP_200_OK)

    def test_admin_can_filter_countries_len(self):
        self.assertEqual(len(self.user_response.data), 1)

    def test_admin_can_filter_countries_name(self):
        self.assertEqual(self.user_response.data[0]["name"], "Test Country 1")

    def test_authenticated_user_can_filter_countries_status(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_filter_countries_len(self):
        self.assertEqual(len(self.response.data), 1)

    def test_authenticated_user_can_filter_countries_name(self):
        self.assertEqual(self.response.data[0]["name"], "Test Country 1")

    def test_non_authenticated_user_can_filter_countries(self):
        self.client.logout()
        response = self.client.get(
            reverse("airport:country-list"), {"country": "Test Country 1"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
