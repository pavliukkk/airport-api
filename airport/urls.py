from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirplaneTypeViewSet,
    FlightViewSet,
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    OrderViewSet,
    AirplaneViewSet,
)

router = routers.DefaultRouter()
router.register("airplane_types", AirplaneTypeViewSet)
router.register("flights", FlightViewSet)
router.register("crews", CrewViewSet)
router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("routes", RouteViewSet)
router.register("orders", OrderViewSet)


urlpatterns = (
    [
        path("", include(router.urls)),
    ]
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

app_name = "airport"
