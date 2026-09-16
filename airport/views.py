from rest_framework import viewsets

from airport.models import (
    AirplaneType,
    Airport,
    Route,
    Crew,
    Ticket,
    Airplane,
    Flight,
    Order,
)
from airport.serializers import (
    AirplaneTypeSerializer,
    AirportSerializer,
    RouteSerializer,
    CrewSerializer,
    TicketSerializer,
    AirplaneSerializer,
    FlightSerializer,
    OrderSerializer,
)


class AirplaneTypeViewSet(
    viewsets.ModelViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirportViewSet(
    viewsets.ModelViewSet,
):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(
    viewsets.ModelViewSet,
):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class CrewViewSet(
    viewsets.ModelViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class TicketViewSet(
    viewsets.ModelViewSet,
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class AirplaneViewSet(
    viewsets.ModelViewSet,
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class OrderViewSet(
    viewsets.ModelViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class FlightViewSet(
    viewsets.ModelViewSet,
):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
