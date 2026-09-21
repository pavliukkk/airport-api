from django.db.models import Count, F
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import mixins, status, viewsets
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


@extend_schema(tags=["Airplane Types"])
class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

    @extend_schema(
        summary="List airplane types",
        description="Returns all airplane types.",
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter airplane types by name.",
                required=False,
                type=str,
            ),
        ],
        responses={200: AirplaneTypeSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create airplane type",
        description="Creates a new airplane type.",
        request=AirplaneTypeSerializer,
        responses={
            201: AirplaneTypeSerializer,
            400: OpenApiResponse(description="Invalid data."),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve airplane type",
        description="Returns an airplane type by ID.",
        responses={
            200: AirplaneTypeSerializer,
            404: OpenApiResponse(description="Airplane type not found."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update airplane type",
        description="Updates an airplane type.",
        request=AirplaneTypeSerializer,
        responses={
            200: AirplaneTypeSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Airplane type not found."),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update airplane type",
        description="Partially updates an airplane type.",
        request=AirplaneTypeSerializer,
        responses={
            200: AirplaneTypeSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Airplane type not found."),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete airplane type",
        description="Deletes an airplane type.",
        responses={
            204: OpenApiResponse(description="Airplane type deleted."),
            404: OpenApiResponse(description="Airplane type not found."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


@extend_schema(tags=["Airports"])
class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    @extend_schema(
        summary="List airports",
        description="Returns all airports.",
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter airports by name.",
                required=False,
                type=str,
            ),
        ],
        responses={200: AirportSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create airport",
        description="Creates a new airport.",
        request=AirportSerializer,
        responses={
            201: AirportSerializer,
            400: OpenApiResponse(description="Invalid data."),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve airport",
        description="Returns an airport by ID.",
        responses={
            200: AirportSerializer,
            404: OpenApiResponse(description="Airport not found."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update airport",
        description="Updates an airport.",
        request=AirportSerializer,
        responses={
            200: AirportSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Airport not found."),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update airport",
        description="Partially updates an airport.",
        request=AirportSerializer,
        responses={
            200: AirportSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Airport not found."),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete airport",
        description="Deletes an airport.",
        responses={
            204: OpenApiResponse(description="Airport deleted."),
            404: OpenApiResponse(description="Airport not found."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        airport_name = self.request.query_params.get("name")

        if airport_name:
            queryset = queryset.filter(name__icontains=airport_name)

        return queryset


@extend_schema(tags=["Routes"])
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

    @extend_schema(
        summary="List routes",
        description="Returns all routes.",
        parameters=[
            OpenApiParameter(
                name="source",
                description="Filter routes by source airport name.",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="destination",
                description="Filter routes by destination airport name.",
                required=False,
                type=str,
            ),
        ],
        responses={200: RouteListSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create route",
        description="Creates a new route between two airports.",
        request=RouteSerializer,
        responses={
            201: RouteSerializer,
            400: OpenApiResponse(description="Invalid data."),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve route",
        description="Returns detailed information about a route.",
        responses={
            200: RouteDetailSerializer,
            404: OpenApiResponse(description="Route not found."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update route",
        description="Updates a route.",
        request=RouteSerializer,
        responses={
            200: RouteSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Route not found."),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update route",
        description="Partially updates a route.",
        request=RouteSerializer,
        responses={
            200: RouteSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Route not found."),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete route",
        description="Deletes a route.",
        responses={
            204: OpenApiResponse(description="Route deleted."),
            404: OpenApiResponse(description="Route not found."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
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


@extend_schema(tags=["Crew"])
class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    @extend_schema(
        summary="List crew members",
        description="Returns all crew members.",
        responses={200: CrewSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create crew member",
        description="Creates a new crew member.",
        request=CrewSerializer,
        responses={
            201: CrewSerializer,
            400: OpenApiResponse(description="Invalid data."),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve crew member",
        description="Returns a crew member by ID.",
        responses={
            200: CrewSerializer,
            404: OpenApiResponse(description="Crew member not found."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update crew member",
        description="Updates a crew member.",
        request=CrewSerializer,
        responses={
            200: CrewSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Crew member not found."),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update crew member",
        description="Partially updates a crew member.",
        request=CrewSerializer,
        responses={
            200: CrewSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Crew member not found."),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete crew member",
        description="Deletes a crew member.",
        responses={
            204: OpenApiResponse(description="Crew member deleted."),
            404: OpenApiResponse(description="Crew member not found."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["Airplanes"])
class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related()
    serializer_class = AirplaneSerializer

    @extend_schema(
        summary="List airplanes",
        description="Returns all airplanes.",
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter airplanes by name.",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="airplane_type",
                description="Filter by airplane type name.",
                required=False,
                type=str,
            ),
        ],
        responses={200: AirplaneSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create airplane",
        description="Creates a new airplane.",
        request=AirplaneSerializer,
        responses={
            201: AirplaneSerializer,
            400: OpenApiResponse(description="Invalid data."),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve airplane",
        description="Returns an airplane by ID.",
        responses={
            200: AirplaneSerializer,
            404: OpenApiResponse(description="Airplane not found."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update airplane",
        description="Updates an airplane.",
        request=AirplaneSerializer,
        responses={
            200: AirplaneSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Airplane not found."),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update airplane",
        description="Partially updates an airplane.",
        request=AirplaneSerializer,
        responses={
            200: AirplaneSerializer,
            400: OpenApiResponse(description="Invalid data."),
            404: OpenApiResponse(description="Airplane not found."),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete airplane",
        description="Deletes an airplane.",
        responses={
            204: OpenApiResponse(description="Airplane deleted."),
            404: OpenApiResponse(description="Airplane not found."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Upload airplane image",
        description=(
            "Uploads an image for an airplane. "
            "Only administrators can use this endpoint."
        ),
        request=AirplaneImageSerializer,
        responses={
            200: AirplaneImageSerializer,
            400: OpenApiResponse(description="Invalid image data."),
            404: OpenApiResponse(description="Airplane not found."),
        },
    )
    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        item = self.get_object()

        serializer = self.get_serializer(
            item,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_serializer_class(self):
        if self.action == "upload_image":
            return AirplaneImageSerializer

        return AirplaneSerializer

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get("name")
        airplane_type = self.request.query_params.get("airplane_type")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if airplane_type:
            queryset = queryset.filter(airplane_type__name__icontains=airplane_type)

        return queryset


@extend_schema(tags=["Orders"])
class OrderViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Order.objects.prefetch_related("tickets")
    serializer_class = OrderSerializer

    @extend_schema(
        summary="List orders",
        description=("Returns all orders belonging to " "the authenticated user."),
        responses={200: OrderSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create order",
        description=("Creates an order with tickets " "for the authenticated user."),
        request=OrderSerializer,
        responses={
            201: OrderSerializer,
            400: OpenApiResponse(description="Invalid order data."),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve order",
        description=("Returns an order belonging to " "the authenticated user."),
        responses={
            200: OrderDetailSerializer,
            404: OpenApiResponse(description="Order not found."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Delete order",
        description=("Deletes an order belonging to " "the authenticated user."),
        responses={
            204: OpenApiResponse(description="Order deleted."),
            404: OpenApiResponse(description="Order not found."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializer

    def get_queryset(self):
        return Order.objects.prefetch_related("tickets").filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Flights"])
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

    @extend_schema(
        summary="List flights",
        description=(
            "Returns all flights with the number "
            "of available tickets. "
            "Available tickets are calculated as "
            "airplane capacity minus booked tickets."
        ),
        responses={200: FlightListSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create flight",
        description="Creates a new flight.",
        request=FlightSerializer,
        responses={
            201: FlightSerializer,
            400: OpenApiResponse(description="Invalid flight data."),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve flight",
        description="Returns detailed information about a flight.",
        responses={
            200: FlightDetailSerializer,
            404: OpenApiResponse(description="Flight not found."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.annotate(
                tickets_available=(
                    F("airplane__rows") * F("airplane__seats_in_row") - Count("tickets")
                )
            ).order_by("id")

        return queryset
