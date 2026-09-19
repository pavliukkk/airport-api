from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    AirplaneType,
    Airport,
    Route,
    Crew,
    Order,
    Ticket,
    Airplane,
    Flight,
)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"

    def validate(self, attrs):
        if AirplaneType.objects.filter(
            name=attrs["name"],
        ).exists():
            raise ValidationError("Airplane type with this name already exists.")
        return attrs


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="name",
        queryset=AirplaneType.objects.all(),
    )

    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats_in_row", "airplane_type", "capacity"]

    def validate(self, attrs):
        if Airplane.objects.filter(
            name=attrs["name"],
            rows=attrs["rows"],
            seats_in_row=attrs["seats_in_row"],
            airplane_type=attrs["airplane_type"].id,
        ).exists():
            raise ValidationError("Airplane type with this data already exists.")
        return attrs


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"

    def validate(self, attrs):
        data = super(AirportSerializer, self).validate(attrs=attrs)
        Airport.validate_closest_big_city(
            attrs["closest_big_city"],
            ValidationError,
        )
        return data


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        queryset=Airport.objects.all(),
        slug_field="name",
    )
    destination = serializers.SlugRelatedField(
        queryset=Airport.objects.all(),
        slug_field="name",
    )

    def validate(self, attrs):
        data = super(RouteSerializer, self).validate(attrs=attrs)
        Route.validate_route(
            attrs["source"],
            attrs["destination"],
            ValidationError,
        )
        if Route.objects.filter(
            source=attrs["source"].id,
            destination=attrs["destination"].id,
        ).exists():
            raise ValidationError("Airport with these data already exists.")
        return data

    class Meta:
        model = Route
        fields = [
            "id",
            "source",
            "destination",
            "distance",
        ]


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    destination = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Route
        fields = [
            "id",
            "source",
            "destination",
            "distance",
        ]


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)

    class Meta:
        model = Route
        fields = [
            "id",
            "source",
            "destination",
            "distance",
        ]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
        ]


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"],
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.select_related(
            "source",
            "destination",
        )
    )

    class Meta:
        model = Flight
        fields = [
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "airplane",
        ]


class FlightListSerializer(FlightSerializer):
    airplane = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    source = serializers.CharField(read_only=True, source="route.source.name")
    destination = serializers.CharField(read_only=True, source="route.destination.name")
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = [
            "id",
            "departure_time",
            "arrival_time",
            "source",
            "destination",
            "airplane",
            "tickets_available",
        ]


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = serializers.SerializerMethodField(read_only=True)
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    taken_seats = serializers.SlugRelatedField(
        source="tickets", many=True, read_only=True, slug_field="seat"
    )

    class Meta:
        model = Flight
        fields = [
            "id",
            "departure_time",
            "arrival_time",
            "route",
            "airplane",
            "crew",
            "taken_seats",
        ]

    def get_airplane(self, obj):
        return {
            "name": obj.airplane.name,
            "airplane_type": obj.airplane.airplane_type.name,
        }


class TicketDetailSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)

            for ticket_data in tickets_data:
                Ticket.objects.create(
                    order=order,
                    **ticket_data,
                )

            return order


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")
