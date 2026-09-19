from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["first_name", "last_name"]


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                condition=Q(closest_big_city__regex=r"^[A-Za-z ]+$"),
                name="closest_big_city must have only letters",
            )
        ]

    @staticmethod
    def validate_closest_big_city(closest_big_city, error_to_raise):
        if not all(c.isalpha() or c.isspace() for c in closest_big_city):
            raise error_to_raise(
                {
                    "closest_big_city_has_numbers": f"closest_big_city must have only letters or (and) spaces."
                }
            )


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source_routes",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="destination_routes",
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} -> {self.destination} ({self.distance} km)"

    class Meta:
        ordering = ["distance"]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(source=models.F("destination")),
                name="source_different_from_destination",
            )
        ]

    @staticmethod
    def validate_route(source, destination, error_to_raise):
        if source == destination:
            raise error_to_raise(
                {
                    "source_different_from_destination": "Source and destination must be different."
                }
            )


class AirplaneType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes",
    )

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} ({self.capacity} seats)"

    class Meta:
        ordering = ["name"]


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def __str__(self):
        return f"{self.user} {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    crew = models.ManyToManyField(
        Crew,
        related_name="flights",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        route = self._state.fields_cache.get("route")
        airplane = self._state.fields_cache.get("airplane")

        if route is not None and airplane is not None:
            return f"{route} {airplane.name}"

        return f"Flight #{self.pk}"

    class Meta:
        ordering = ["departure_time"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    @staticmethod
    def validate_ticket(row, seat, flight, error_to_raise):
        for ticket_attr_value, ticket_attr_name, flight_attr_name in [
            (row, "row", "id"),
            (seat, "seat", "id"),
        ]:
            count_attrs = getattr(flight, flight_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {flight_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight,
            ValidationError,
        )

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super().save(
            *args,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self):
        return f"{self.row} {self.seat}"

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]
