from django.db.models import Count, F
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from airport.models import (
    AirplaneType,
    Airport,
    Route,
    Crew,
    Airplane,
    Flight,
    Order,
)
from airport.permissions import IsAuthenticatedReadOnlyOrIsAdmin
from airport.renders import CustomBrowsableAPIRenderer
from airport.serializers import (
    AirplaneTypeSerializer,
    AirportSerializer,
    RouteSerializer,
    CrewSerializer,
    AirplaneSerializer,
    FlightSerializer,
    OrderSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    OrderDetailSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    AirplaneImageSerializer,
)


class AirplaneTypeViewSet(
    viewsets.ModelViewSet,
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAuthenticatedReadOnlyOrIsAdmin,)

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class AirportViewSet(
    viewsets.ModelViewSet,
):
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticatedReadOnlyOrIsAdmin,)
    queryset = Airport.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        airport_name = self.request.query_params.get("name")
        if airport_name:
            queryset = queryset.filter(name__icontains=airport_name)
        return queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related(
        "source",
        "destination",
    )
    serializer_class = RouteSerializer
    renderer_classes = [
        JSONRenderer,
        CustomBrowsableAPIRenderer,
    ]
    permission_classes = (IsAuthenticatedReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        if source:
            queryset = queryset.filter(source__name__icontains=source)

        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        return queryset


class CrewViewSet(
    viewsets.ModelViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAuthenticatedReadOnlyOrIsAdmin,)


class AirplaneViewSet(
    viewsets.ModelViewSet,
):
    queryset = Airplane.objects.select_related()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAuthenticatedReadOnlyOrIsAdmin,)

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")
        airplane_type = self.request.query_params.get("airplane_type")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if airplane_type:
            queryset = queryset.filter(airplane_type__name__icontains=airplane_type)

        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return AirplaneImageSerializer
        return AirplaneSerializer


class OrderViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Order.objects.prefetch_related("tickets")
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.prefetch_related("tickets").filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlightViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Flight.objects.select_related(
        "route",
        "route__source",
        "route__destination",
        "airplane",
    ).prefetch_related("crew")
    serializer_class = FlightSerializer
    permission_classes = (IsAuthenticatedReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset.annotate(
                    tickets_available=F("airplane__rows") * F("airplane__seats_in_row")
                    - Count("tickets")
                )
            ).order_by("id")
        return queryset
