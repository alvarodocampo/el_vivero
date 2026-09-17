from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


# =========================================================
# PERFIL DEL HUÉSPED
# =========================================================

class GuestProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guest_profile",
        verbose_name="Usuario"
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Teléfono"
    )

    admin_notes = models.TextField(
        blank=True,
        verbose_name="Observaciones internas",
        help_text=(
            "Notas privadas sobre el huésped visibles "
            "únicamente para los administradores."
        )
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro"
    )

    def __str__(self):
        return self.user.email or str(self.user)


# =========================================================
# RESERVAS
# =========================================================

class Booking(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("confirmed", "Confirmada"),
        ("cancelled", "Cancelada"),
        ("completed", "Finalizada"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Huésped"
    )

    check_in = models.DateField(
        verbose_name="Entrada"
    )

    check_out = models.DateField(
        verbose_name="Salida"
    )

    guests = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name="Número de huéspedes"
    )

    price_per_night = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=100,
        validators=[MinValueValidator(0)],
        verbose_name="Precio por noche",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="confirmed",
        verbose_name="Estado"
    )

    internal_notes = models.TextField(
        blank=True,
        verbose_name="Observaciones de la reserva",
        help_text=(
            "Notas internas específicas de esta estancia."
        )
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:
        ordering = [
            "-created_at"
        ]

        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

        constraints = [
            models.CheckConstraint(
                condition=Q(guests__gte=1, guests__lte=4),
                name="booking_guests_between_1_and_4",
            ),
            models.CheckConstraint(
                condition=Q(check_out__gt=models.F("check_in")),
                name="booking_checkout_after_checkin",
            ),
        ]

    def __str__(self):

        email = (
            self.user.email
            or self.user.username
        )

        return (
            f"{email} | "
            f"{self.check_in} - {self.check_out}"
        )

    @property
    def number_of_nights(self):
        if not self.check_in or not self.check_out:
            return 0
        return (self.check_out - self.check_in).days

    @property
    def total_price(self):
        return self.price_per_night * self.number_of_nights

    def clean(self):
        super().clean()

        if not self.check_in or not self.check_out:
            return

        if self.check_out <= self.check_in:
            raise ValidationError({
                "check_out": "La salida debe ser posterior a la entrada."
            })

        if self.check_in < timezone.localdate():
            raise ValidationError({
                "check_in": "La fecha de entrada no puede estar en el pasado."
            })

        if self.number_of_nights < 2:
            raise ValidationError({
                "check_out": "La estancia mínima es de 2 noches."
            })

        overlaps = Booking.objects.exclude(status="cancelled").filter(
            check_in__lt=self.check_out,
            check_out__gt=self.check_in,
        )
        if self.pk:
            overlaps = overlaps.exclude(pk=self.pk)

        if overlaps.exists() and self.status != "cancelled":
            raise ValidationError(
                "Ya existe una reserva activa que coincide con estas fechas."
            )
