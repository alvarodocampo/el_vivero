from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
from django.db.models import F, Q


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="price_per_night",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("100.00"),
                max_digits=8,
                validators=[MinValueValidator(0)],
                verbose_name="Precio por noche",
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="guests",
            field=models.PositiveIntegerField(
                default=1,
                validators=[MinValueValidator(1), MaxValueValidator(4)],
                verbose_name="Número de huéspedes",
            ),
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.CheckConstraint(
                condition=Q(guests__gte=1, guests__lte=4),
                name="booking_guests_between_1_and_4",
            ),
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.CheckConstraint(
                condition=Q(check_out__gt=F("check_in")),
                name="booking_checkout_after_checkin",
            ),
        ),
    ]
