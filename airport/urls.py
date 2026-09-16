from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirplaneTypeViewSet,
    FlightViewSet,
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    OrderViewSet,
    TicketViewSet,
    AirplaneViewSet,
)

router = routers.DefaultRouter()
router.register("airplane_types", AirplaneTypeViewSet)
router.register("flights", FlightViewSet)
router.register("crews", CrewViewSet)
router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("routes", RouteViewSet)
router.register("tickets", TicketViewSet)
router.register("orders", OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
