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


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Airplane
        fields = [
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
        ]


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = []


class RouteListSerializer(serializers.ModelSerializer):
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


class RouteDetailSerializer(serializers.ModelSerializer):
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
    route = RouteListSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
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
        ]


class FlightDetailSerializer(serializers.ModelSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
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
        ]


class TicketDetailSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at", "user")

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


class OrderDetailSerializer(serializers.ModelSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")
