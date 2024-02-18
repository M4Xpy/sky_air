from django.urls import path, include
from rest_framework import routers

from airport.views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
)

router = routers.DefaultRouter()
router.register("countries", CountryViewSet, )
router.register("cities", CityViewSet, )
router.register("airports", AirportViewSet, )
router.register("routes", RouteViewSet, )
router.register("airplane_types", AirplaneTypeViewSet, )
router.register("airplanes", AirplaneViewSet, )
router.register("crews", CrewViewSet, )

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
