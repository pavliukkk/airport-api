from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from airport.models import (
    Airplane,
    AirplaneType,
    Airport,
    Crew,
    Flight,
    Order,
    Route,
    Ticket,
)

User = get_user_model()


AIRPLANE_TYPE_URL = "/api/airport/airplane_types/"
AIRPORT_URL = "/api/airport/airports/"
ROUTE_URL = "/api/airport/routes/"
CREW_URL = "/api/airport/crews/"
AIRPLANE_URL = "/api/airport/airplanes/"
FLIGHT_URL = "/api/airport/flights/"
ORDER_URL = "/api/airport/orders/"


def detail_url(url, obj_id):
    return f"{url}{obj_id}/"


class BaseViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123",
        )

        self.admin = User.objects.create_superuser(
            email="admin@test.com",
            password="testpass123",
        )

    def authenticate_user(self):
        self.client.force_authenticate(user=self.user)

    def authenticate_admin(self):
        self.client.force_authenticate(user=self.admin)


class AirplaneTypeViewSetTests(BaseViewSetTest):
    def setUp(self):
        super().setUp()

        self.airplane_type = AirplaneType.objects.create(
            name="Boeing",
        )

    def test_user_can_list(self):
        self.authenticate_user()

        response = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve(self):
        self.authenticate_user()

        response = self.client.get(detail_url(AIRPLANE_TYPE_URL, self.airplane_type.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create(self):
        self.authenticate_user()

        response = self.client.post(
            AIRPLANE_TYPE_URL,
            {"name": "Airbus"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update(self):
        self.authenticate_user()

        response = self.client.put(
            detail_url(AIRPLANE_TYPE_URL, self.airplane_type.id),
            {"name": "Airbus"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete(self):
        self.authenticate_user()

        response = self.client.delete(
            detail_url(AIRPLANE_TYPE_URL, self.airplane_type.id)
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create(self):
        self.authenticate_admin()

        response = self.client.post(
            AIRPLANE_TYPE_URL,
            {"name": "Airbus"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update(self):
        self.authenticate_admin()

        response = self.client.put(
            detail_url(AIRPLANE_TYPE_URL, self.airplane_type.id),
            {"name": "Airbus"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete(self):
        self.authenticate_admin()

        response = self.client.delete(
            detail_url(AIRPLANE_TYPE_URL, self.airplane_type.id)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AirportViewSetTests(BaseViewSetTest):
    def setUp(self):
        super().setUp()

        self.airport = Airport.objects.create(
            name="Heathrow",
            closest_big_city="London",
        )

    def test_user_can_list(self):
        self.authenticate_user()

        response = self.client.get(AIRPORT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve(self):
        self.authenticate_user()

        response = self.client.get(detail_url(AIRPORT_URL, self.airport.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create(self):
        self.authenticate_user()

        response = self.client.post(
            AIRPORT_URL,
            {
                "name": "Charles de Gaulle",
                "closest_big_city": "Paris",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update(self):
        self.authenticate_user()

        response = self.client.put(
            detail_url(AIRPORT_URL, self.airport.id),
            {
                "name": "Updated Airport",
                "closest_big_city": "London",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete(self):
        self.authenticate_user()

        response = self.client.delete(detail_url(AIRPORT_URL, self.airport.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create(self):
        self.authenticate_admin()

        response = self.client.post(
            AIRPORT_URL,
            {
                "name": "Charles de Gaulle",
                "closest_big_city": "Paris",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update(self):
        self.authenticate_admin()

        response = self.client.put(
            detail_url(AIRPORT_URL, self.airport.id),
            {
                "name": "Updated Airport",
                "closest_big_city": "London",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_put(self):
        self.authenticate_admin()

        response = self.client.patch(
            detail_url(AIRPORT_URL, self.airport.id),
            {
                "closest_big_city": "London",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete(self):
        self.authenticate_admin()

        response = self.client.delete(detail_url(AIRPORT_URL, self.airport.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RouteViewSetTests(BaseViewSetTest):
    def setUp(self):
        super().setUp()

        self.airport1 = Airport.objects.create(
            name="Heathrow",
            closest_big_city="London",
        )

        self.airport2 = Airport.objects.create(
            name="Charles de Gaulle",
            closest_big_city="Paris",
        )

        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=350,
        )

    def test_user_can_list(self):
        self.authenticate_user()

        response = self.client.get(ROUTE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve(self):
        self.authenticate_user()

        response = self.client.get(detail_url(ROUTE_URL, self.route.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create(self):
        self.authenticate_user()

        airport3 = Airport.objects.create(
            name="Frankfurt",
            closest_big_city="Frankfurt",
        )

        response = self.client.post(
            ROUTE_URL,
            {
                "source": self.airport1.name,
                "destination": airport3.name,
                "distance": 600,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update(self):
        self.authenticate_user()

        response = self.client.put(
            detail_url(ROUTE_URL, self.route.id),
            {
                "source": self.airport1.name,
                "destination": self.airport2.name,
                "distance": 500,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete(self):
        self.authenticate_user()

        response = self.client.delete(detail_url(ROUTE_URL, self.route.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create(self):
        self.authenticate_admin()

        airport3 = Airport.objects.create(
            name="Frankfurt",
            closest_big_city="Frankfurt",
        )

        response = self.client.post(
            ROUTE_URL,
            {
                "source": self.airport1.name,
                "destination": airport3.name,
                "distance": 600,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update(self):
        self.authenticate_admin()

        response = self.client.put(
            detail_url(ROUTE_URL, self.route.id),
            {
                "source": self.airport1.name,
                "destination": self.airport2.name,
                "distance": 500,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete(self):
        self.authenticate_admin()

        response = self.client.delete(detail_url(ROUTE_URL, self.route.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CrewViewSetTests(BaseViewSetTest):
    def setUp(self):
        super().setUp()

        self.crew = Crew.objects.create(
            first_name="John",
            last_name="Smith",
        )

    def test_user_can_list(self):
        self.authenticate_user()

        response = self.client.get(CREW_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve(self):
        self.authenticate_user()

        response = self.client.get(detail_url(CREW_URL, self.crew.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create(self):
        self.authenticate_user()

        response = self.client.post(
            CREW_URL,
            {
                "first_name": "Jane",
                "last_name": "Doe",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update(self):
        self.authenticate_user()

        response = self.client.put(
            detail_url(CREW_URL, self.crew.id),
            {
                "first_name": "Jane",
                "last_name": "Doe",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete(self):
        self.authenticate_user()

        response = self.client.delete(detail_url(CREW_URL, self.crew.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create(self):
        self.authenticate_admin()

        response = self.client.post(
            CREW_URL,
            {
                "first_name": "Jane",
                "last_name": "Doe",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update(self):
        self.authenticate_admin()

        response = self.client.put(
            detail_url(CREW_URL, self.crew.id),
            {
                "first_name": "Jane",
                "last_name": "Doe",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete(self):
        self.authenticate_admin()

        response = self.client.delete(detail_url(CREW_URL, self.crew.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AirplaneViewSetTests(BaseViewSetTest):
    def setUp(self):
        super().setUp()

        self.airplane_type = AirplaneType.objects.create(
            name="Boeing",
        )

        self.airplane = Airplane.objects.create(
            name="Boeing 737",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

    def test_user_can_list(self):
        self.authenticate_user()

        response = self.client.get(AIRPLANE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve(self):
        self.authenticate_user()

        response = self.client.get(detail_url(AIRPLANE_URL, self.airplane.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create(self):
        self.authenticate_user()

        response = self.client.post(
            AIRPLANE_URL,
            {
                "name": "Airbus A320",
                "rows": 10,
                "seats_in_row": 6,
                "airplane_type": self.airplane_type.name,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update(self):
        self.authenticate_user()

        response = self.client.put(
            detail_url(AIRPLANE_URL, self.airplane.id),
            {
                "name": "Airbus A320",
                "rows": 10,
                "seats_in_row": 6,
                "airplane_type": self.airplane_type.name,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete(self):
        self.authenticate_user()

        response = self.client.delete(detail_url(AIRPLANE_URL, self.airplane.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create(self):
        self.authenticate_admin()

        response = self.client.post(
            AIRPLANE_URL,
            {
                "name": "Airbus A320",
                "rows": 10,
                "seats_in_row": 6,
                "airplane_type": self.airplane_type.name,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update(self):
        self.authenticate_admin()

        response = self.client.put(
            detail_url(AIRPLANE_URL, self.airplane.id),
            {
                "name": "Airbus A320",
                "rows": 10,
                "seats_in_row": 6,
                "airplane_type": self.airplane_type.name,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete(self):
        self.authenticate_admin()

        response = self.client.delete(detail_url(AIRPLANE_URL, self.airplane.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_upload_image(self):
        self.authenticate_user()

        image = BytesIO()
        Image.new("RGB", (10, 10)).save(image, format="JPEG")
        image.seek(0)

        response = self.client.post(
            f"{detail_url(AIRPLANE_URL, self.airplane.id)}upload-image/",
            {
                "image": SimpleUploadedFile(
                    "test.jpg",
                    image.read(),
                    content_type="image/jpeg",
                )
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_upload_image(self):
        self.authenticate_admin()

        image = BytesIO()
        Image.new("RGB", (10, 10)).save(image, format="JPEG")
        image.seek(0)

        response = self.client.post(
            f"{detail_url(AIRPLANE_URL, self.airplane.id)}upload-image/",
            {
                "image": SimpleUploadedFile(
                    "test.jpg",
                    image.read(),
                    content_type="image/jpeg",
                )
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FlightViewSetTests(BaseViewSetTest):
    def setUp(self):
        super().setUp()

        self.airport1 = Airport.objects.create(
            name="Heathrow",
            closest_big_city="London",
        )

        self.airport2 = Airport.objects.create(
            name="Charles de Gaulle",
            closest_big_city="Paris",
        )

        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=350,
        )

        self.airplane_type = AirplaneType.objects.create(
            name="Boeing",
        )

        self.airplane = Airplane.objects.create(
            name="Boeing 737",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

        self.crew = Crew.objects.create(
            first_name="John",
            last_name="Smith",
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2026-10-01T10:00:00Z",
            arrival_time="2026-10-01T12:00:00Z",
        )

        self.flight.crew.add(self.crew)

    def test_user_can_list(self):
        self.authenticate_user()

        response = self.client.get(FLIGHT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve(self):
        self.authenticate_user()

        response = self.client.get(detail_url(FLIGHT_URL, self.flight.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create(self):
        self.authenticate_user()

        response = self.client.post(
            FLIGHT_URL,
            {
                "route": self.route.id,
                "airplane": self.airplane.id,
                "departure_time": "2026-10-02T10:00:00Z",
                "arrival_time": "2026-10-02T12:00:00Z",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create(self):
        self.authenticate_admin()

        response = self.client.post(
            FLIGHT_URL,
            {
                "route": self.route.id,
                "airplane": self.airplane.id,
                "departure_time": "2026-10-02T10:00:00Z",
                "arrival_time": "2026-10-02T12:00:00Z",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderViewSetTests(BaseViewSetTest):
    def setUp(self):
        super().setUp()

        self.airport1 = Airport.objects.create(
            name="Heathrow",
            closest_big_city="London",
        )

        self.airport2 = Airport.objects.create(
            name="Charles de Gaulle",
            closest_big_city="Paris",
        )

        self.route = Route.objects.create(
            source=self.airport1,
            destination=self.airport2,
            distance=350,
        )

        self.airplane_type = AirplaneType.objects.create(
            name="Boeing",
        )

        self.airplane = Airplane.objects.create(
            name="Boeing 737",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2026-10-01T10:00:00Z",
            arrival_time="2026-10-01T12:00:00Z",
        )

        self.order = Order.objects.create(
            user=self.user,
        )

        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=self.order,
        )

    def test_user_can_list_own_orders(self):
        self.authenticate_user()

        response = self.client.get(ORDER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_own_order(self):
        self.authenticate_user()

        response = self.client.get(detail_url(ORDER_URL, self.order.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_order(self):
        self.authenticate_user()

        response = self.client.post(
            ORDER_URL,
            {
                "tickets": [
                    {
                        "row": 2,
                        "seat": 2,
                        "flight": self.flight.id,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_delete_own_order(self):
        self.authenticate_user()

        response = self.client.delete(detail_url(ORDER_URL, self.order.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_access_other_order(self):
        other_user = User.objects.create_user(
            email="other@test.com",
            password="testpass123",
        )

        other_order = Order.objects.create(
            user=other_user,
        )

        self.authenticate_user()

        response = self.client.get(detail_url(ORDER_URL, other_order.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_other_order(self):
        other_user = User.objects.create_user(
            email="other@test.com",
            password="testpass123",
        )

        other_order = Order.objects.create(
            user=other_user,
        )

        self.authenticate_user()

        response = self.client.delete(detail_url(ORDER_URL, other_order.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_list_own_orders(self):
        self.authenticate_admin()

        response = self.client.get(ORDER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_order(self):
        self.authenticate_admin()

        response = self.client.post(
            ORDER_URL,
            {
                "tickets": [
                    {
                        "row": 3,
                        "seat": 3,
                        "flight": self.flight.id,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
