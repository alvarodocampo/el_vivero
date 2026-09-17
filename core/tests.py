from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Booking


@override_settings(DEFAULT_PRICE_PER_NIGHT="100.00")
class BookingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="huesped",
            email="huesped@example.com",
            password="UnaClaveSegura123!",
        )
        self.check_in = date.today() + timedelta(days=30)
        self.check_out = self.check_in + timedelta(days=3)

    def booking(self, **changes):
        values = {
            "user": self.user,
            "check_in": self.check_in,
            "check_out": self.check_out,
            "guests": 2,
            "price_per_night": Decimal("100.00"),
        }
        values.update(changes)
        return Booking(**values)

    def test_calculates_nights_and_total(self):
        booking = self.booking()
        self.assertEqual(booking.number_of_nights, 3)
        self.assertEqual(booking.total_price, Decimal("300.00"))

    def test_rejects_stays_shorter_than_two_nights(self):
        booking = self.booking(check_out=self.check_in + timedelta(days=1))
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_rejects_past_check_in(self):
        booking = self.booking(
            check_in=date.today() - timedelta(days=3),
            check_out=date.today() - timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_rejects_more_than_four_guests(self):
        booking = self.booking(guests=5)
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_rejects_overlapping_active_booking(self):
        Booking.objects.create(
            user=self.user,
            check_in=self.check_in,
            check_out=self.check_out,
            guests=2,
        )
        booking = self.booking(
            check_in=self.check_in + timedelta(days=1),
            check_out=self.check_out + timedelta(days=1),
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_cancelled_booking_does_not_block_dates(self):
        Booking.objects.create(
            user=self.user,
            check_in=self.check_in,
            check_out=self.check_out,
            guests=2,
            status="cancelled",
        )
        self.booking().full_clean()

    def test_booking_api_requires_login(self):
        response = self.client.post(reverse("create_booking"), {})
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_create_booking(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("create_booking"),
            {
                "phone": "600123123",
                "check_in": self.check_in.isoformat(),
                "check_out": self.check_out.isoformat(),
                "guests": "2",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["total_price"], "300.00")

    def test_my_bookings_api_returns_only_current_users_data(self):
        Booking.objects.create(
            user=self.user,
            check_in=self.check_in,
            check_out=self.check_out,
            guests=2,
        )
        self.client.force_login(self.user)
        response = self.client.get(reverse("my_bookings"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["bookings"]), 1)

    def test_admin_booking_pages_load(self):
        admin_user = get_user_model().objects.create_superuser(
            username="admin_test",
            email="admin@example.com",
            password="UnaClaveSegura123!",
        )
        self.client.force_login(admin_user)
        response = self.client.get("/admin/core/booking/")
        self.assertEqual(response.status_code, 200)

# Create your tests here.
