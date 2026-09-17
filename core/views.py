from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from .models import Booking, GuestProfile


def home(request):
    return render(request, "core/home.html")


def disponibilidad(request):
    return render(request, "core/disponibilidad.html")


def mis_reservas(request):
    return render(request, "core/mis_reservas.html")


def informacion(request):
    return render(request, "core/informacion.html")


def contacto(request):
    return render(request, "core/contacto.html")


def normas(request):
    return render(request, "core/normas.html")


def fotos(request):
    return render(request, "core/fotos.html")


def extras(request):
    return render(request, "core/extras.html")


def preguntas_frecuentes(request):
    return render(request, "core/preguntas_frecuentes.html")


# =========================================================
# FECHAS OCUPADAS
# =========================================================

def occupied_dates(request):

    bookings = Booking.objects.exclude(
        status="cancelled"
    )

    dates = []

    for booking in bookings:

        current_date = booking.check_in

        while current_date < booking.check_out:

            dates.append(
                current_date.isoformat()
            )

            current_date += timedelta(days=1)

    return JsonResponse({
        "occupied_dates": dates
    })


def my_bookings(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"detail": "Debes iniciar sesión."},
            status=401,
        )

    bookings = request.user.bookings.order_by("-check_in")
    data = [
        {
            "id": booking.id,
            "reference": f"EV-{booking.id:05d}",
            "check_in": booking.check_in.isoformat(),
            "check_out": booking.check_out.isoformat(),
            "nights": booking.number_of_nights,
            "guests": booking.guests,
            "status": booking.status,
            "status_label": booking.get_status_display(),
            "price_per_night": str(booking.price_per_night),
            "total_price": str(booking.total_price),
        }
        for booking in bookings
    ]
    return JsonResponse({"bookings": data})


# =========================================================
# CREAR RESERVA
# =========================================================

@require_POST
def create_booking(request):

    # =====================================================
    # COMPROBAR QUE EL USUARIO HA INICIADO SESIÓN
    # =====================================================

    if not request.user.is_authenticated:

        return JsonResponse(
            {
                "success": False,
                "login_required": True,
                "message": (
                    "Debes iniciar sesión o crear una cuenta "
                    "antes de realizar una reserva."
                ),
            },
            status=401,
        )


    # =====================================================
    # RECIBIR DATOS
    # =====================================================

    phone = request.POST.get(
        "phone",
        ""
    ).strip()


    check_in = parse_date(
        request.POST.get(
            "check_in",
            ""
        )
    )


    check_out = parse_date(
        request.POST.get(
            "check_out",
            ""
        )
    )


    try:

        guests = int(
            request.POST.get(
                "guests",
                0
            )
        )

    except (TypeError, ValueError):

        guests = 0


    # =====================================================
    # VALIDAR TELÉFONO
    # =====================================================

    if not phone:

        return JsonResponse(
            {
                "success": False,
                "message": "Introduce tu teléfono."
            },
            status=400,
        )


    # =====================================================
    # VALIDAR FECHAS
    # =====================================================

    if not check_in or not check_out:

        return JsonResponse(
            {
                "success": False,
                "message": "Las fechas no son válidas."
            },
            status=400,
        )


    if check_out <= check_in:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "La fecha de salida debe ser "
                    "posterior a la entrada."
                ),
            },
            status=400,
        )

    if check_in < timezone.localdate():
        return JsonResponse(
            {
                "success": False,
                "message": "La fecha de entrada no puede estar en el pasado.",
            },
            status=400,
        )


    # =====================================================
    # RESERVA MÍNIMA: 2 NOCHES
    # =====================================================

    nights = (
        check_out -
        check_in
    ).days


    if nights < 2:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "La estancia mínima es de 2 noches."
                ),
            },
            status=400,
        )


    # =====================================================
    # VALIDAR HUÉSPEDES
    # =====================================================

    if guests < 1 or guests > 4:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "El número de huéspedes debe "
                    "estar entre 1 y 4."
                ),
            },
            status=400,
        )


    # =====================================================
    # COMPROBAR SOLAPAMIENTOS Y CREAR RESERVA
    # =====================================================

    with transaction.atomic():

        overlap = Booking.objects.exclude(
            status="cancelled"
        ).filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()


        if overlap:

            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        "Lo sentimos. Estas fechas "
                        "ya no están disponibles."
                    ),
                },
                status=409,
            )


        # =================================================
        # PERFIL DEL HUÉSPED
        # =================================================

        profile, created = (
            GuestProfile.objects.get_or_create(
                user=request.user
            )
        )


        if profile.phone != phone:

            profile.phone = phone

            profile.save(
                update_fields=[
                    "phone"
                ]
            )


        # =================================================
        # CREAR RESERVA
        # =================================================

        booking = Booking.objects.create(
            user=request.user,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            price_per_night=Decimal(settings.DEFAULT_PRICE_PER_NIGHT),
            status="confirmed"
        )


    # =====================================================
    # RESPUESTA
    # =====================================================

    return JsonResponse(
        {
            "success": True,
            "message": (
                "Reserva realizada correctamente."
            ),
            "booking_id": booking.id,
            "total_price": str(booking.total_price),
        }
    )
