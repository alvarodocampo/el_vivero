from django.urls import path

from . import views


urlpatterns = [

    # =========================================================
    # PÁGINA PRINCIPAL
    # =========================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =========================================================
    # DISPONIBILIDAD
    # =========================================================

    path(
        "disponibilidad/",
        views.disponibilidad,
        name="disponibilidad"
    ),

    path(
        "mis-reservas/",
        views.mis_reservas,
        name="mis_reservas"
    ),


    # =========================================================
    # INFORMACIÓN
    # =========================================================

    path(
        "informacion/",
        views.informacion,
        name="informacion"
    ),

    path(
        "informacion/normas/",
        views.normas,
        name="normas"
    ),

    path(
        "informacion/fotos/",
        views.fotos,
        name="fotos"
    ),

    path(
        "informacion/extras/",
        views.extras,
        name="extras"
    ),

    path(
        "informacion/preguntas-frecuentes/",
        views.preguntas_frecuentes,
        name="preguntas_frecuentes"
    ),


    # =========================================================
    # CONTACTO
    # =========================================================

    path(
        "contacto/",
        views.contacto,
        name="contacto"
    ),


    # =========================================================
    # API - FECHAS OCUPADAS
    # =========================================================

    path(
        "api/fechas-ocupadas/",
        views.occupied_dates,
        name="occupied_dates"
    ),

    path(
        "api/mis-reservas/",
        views.my_bookings,
        name="my_bookings"
    ),


    # =========================================================
    # API - CREAR RESERVA
    # =========================================================

    path(
        "api/reservar/",
        views.create_booking,
        name="create_booking"
    ),

]
