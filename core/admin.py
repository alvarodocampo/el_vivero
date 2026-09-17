from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html, format_html_join

from .models import Booking, GuestProfile


# =========================================================
# IDENTIDAD DEL PANEL DE ADMINISTRACIÓN
# =========================================================

admin.site.site_header = "Administración de El Vivero"
admin.site.site_title = "El Vivero"
admin.site.index_title = "Panel de gestión del alojamiento"


# =========================================================
# HUÉSPEDES
# =========================================================

@admin.register(GuestProfile)
class GuestProfileAdmin(admin.ModelAdmin):

    list_display = (
        "guest_name",
        "guest_email",
        "phone",
        "number_of_bookings",
        "returning_guest_badge",
        "created_at",
    )

    list_display_links = (
        "guest_name",
        "guest_email",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone",
        "admin_notes",
    )

    autocomplete_fields = (
        "user",
    )

    readonly_fields = (
        "guest_name",
        "guest_email",
        "number_of_bookings",
        "returning_guest_badge",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25
    save_on_top = True
    preserve_filters = True
    empty_value_display = "—"

    fieldsets = (
        (
            "Datos del huésped",
            {
                "fields": (
                    "user",
                    "guest_name",
                    "guest_email",
                    "phone",
                )
            },
        ),
        (
            "Historial de reservas",
            {
                "fields": (
                    "number_of_bookings",
                    "returning_guest_badge",
                    "created_at",
                )
            },
        ),
        (
            "Observaciones internas",
            {
                "fields": (
                    "admin_notes",
                ),
                "description": (
                    "Estas notas solo son visibles para los "
                    "administradores de El Vivero."
                ),
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return (
            queryset
            .select_related("user")
            .annotate(
                bookings_count=Count(
                    "user__bookings",
                    distinct=True,
                )
            )
        )

    @admin.display(
        description="Nombre",
        ordering="user__first_name",
    )
    def guest_name(self, obj):
        full_name = obj.user.get_full_name().strip()

        return (
            full_name
            or obj.user.username
            or obj.user.email
            or "Sin nombre"
        )

    @admin.display(
        description="Correo electrónico",
        ordering="user__email",
    )
    def guest_email(self, obj):
        return obj.user.email or "Sin correo"

    @admin.display(
        description="Reservas",
        ordering="bookings_count",
    )
    def number_of_bookings(self, obj):
        if hasattr(obj, "bookings_count"):
            return obj.bookings_count

        return obj.user.bookings.count()

    @admin.display(
        description="Tipo de huésped",
    )
    def returning_guest_badge(self, obj):
        total = (
            obj.bookings_count
            if hasattr(obj, "bookings_count")
            else obj.user.bookings.count()
        )

        if total > 1:
            return format_html(
                '<span class="vivero-badge vivero-badge-repeat">'
                "Recurrente · {} reservas"
                "</span>",
                total,
            )

        if total == 1:
            return format_html(
                '<span class="vivero-badge vivero-badge-new">{}</span>',
                "Primera reserva",
            )

        return format_html(
            '<span class="vivero-badge vivero-badge-empty">{}</span>',
            "Sin reservas",
        )

    class Media:
        css = {
            "all": (
                "core/css/el_vivero_admin.css",
            )
        }


# =========================================================
# RESERVAS
# =========================================================

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "booking_reference",
        "guest_name",
        "guest_email",
        "guest_phone",
        "check_in",
        "check_out",
        "number_of_nights",
        "guests",
        "price_per_night",
        "total_price_display",
        "status_badge",
        "returning_guest_badge",
        "created_at",
    )

    list_display_links = (
        "booking_reference",
        "guest_name",
    )

    list_filter = (
        "status",
        "check_in",
        "check_out",
        "guests",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__guest_profile__phone",
        "internal_notes",
    )

    autocomplete_fields = (
        "user",
    )

    readonly_fields = (
        "booking_reference",
        "guest_name",
        "guest_email",
        "guest_phone",
        "number_of_nights",
        "total_price_display",
        "previous_bookings",
        "returning_guest_badge",
        "created_at",
    )

    ordering = (
        "-check_in",
        "-created_at",
    )

    date_hierarchy = "check_in"

    list_select_related = (
        "user",
        "user__guest_profile",
    )

    list_per_page = 25
    save_on_top = True
    preserve_filters = True
    empty_value_display = "—"

    actions = (
        "mark_as_pending",
        "mark_as_confirmed",
        "mark_as_cancelled",
        "mark_as_completed",
    )

    fieldsets = (
        (
            "Datos de la reserva",
            {
                "fields": (
                    "booking_reference",
                    "user",
                    (
                        "check_in",
                        "check_out",
                    ),
                    (
                        "number_of_nights",
                        "guests",
                    ),
                    (
                        "price_per_night",
                        "total_price_display",
                    ),
                    "status",
                )
            },
        ),
        (
            "Datos del huésped",
            {
                "fields": (
                    "guest_name",
                    "guest_email",
                    "guest_phone",
                )
            },
        ),
        (
            "Historial del huésped",
            {
                "fields": (
                    "previous_bookings",
                    "returning_guest_badge",
                )
            },
        ),
        (
            "Observaciones de esta estancia",
            {
                "fields": (
                    "internal_notes",
                ),
                "description": (
                    "Estas observaciones son internas y no "
                    "se muestran ni se envían al huésped."
                ),
            },
        ),
        (
            "Información del sistema",
            {
                "fields": (
                    "created_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return (
            queryset
            .select_related(
                "user",
                "user__guest_profile",
            )
            .annotate(
                user_bookings_count=Count(
                    "user__bookings",
                    distinct=True,
                )
            )
        )

    @admin.display(
        description="Reserva",
        ordering="id",
    )
    def booking_reference(self, obj):
        if not obj.pk:
            return "Nueva reserva"

        return f"EV-{obj.pk:05d}"

    @admin.display(
        description="Nombre",
        ordering="user__first_name",
    )
    def guest_name(self, obj):
        full_name = obj.user.get_full_name().strip()

        return (
            full_name
            or obj.user.username
            or obj.user.email
            or "Sin nombre"
        )

    @admin.display(
        description="Correo electrónico",
        ordering="user__email",
    )
    def guest_email(self, obj):
        return obj.user.email or "Sin correo"

    @admin.display(
        description="Teléfono",
    )
    def guest_phone(self, obj):
        profile = getattr(
            obj.user,
            "guest_profile",
            None,
        )

        if profile is None:
            return "Sin perfil"

        return profile.phone or "Sin teléfono"

    @admin.display(
        description="Noches",
    )
    def number_of_nights(self, obj):
        if not obj.check_in or not obj.check_out:
            return "—"

        nights = (
            obj.check_out -
            obj.check_in
        ).days

        if nights < 0:
            return "Fechas incorrectas"

        return nights

    @admin.display(description="Precio total")
    def total_price_display(self, obj):
        return f"{obj.total_price:.2f} €"

    @admin.display(
        description="Estado",
        ordering="status",
    )
    def status_badge(self, obj):
        status_styles = {
            "pending": (
                "Pendiente",
                "vivero-status-pending",
            ),
            "confirmed": (
                "Confirmada",
                "vivero-status-confirmed",
            ),
            "cancelled": (
                "Cancelada",
                "vivero-status-cancelled",
            ),
            "completed": (
                "Finalizada",
                "vivero-status-completed",
            ),
        }

        label, css_class = status_styles.get(
            obj.status,
            (
                obj.get_status_display(),
                "vivero-status-default",
            ),
        )

        return format_html(
            '<span class="vivero-status {}">{}</span>',
            css_class,
            label,
        )

    @admin.display(
        description="Cliente",
    )
    def returning_guest_badge(self, obj):
        total = (
            obj.user_bookings_count
            if hasattr(obj, "user_bookings_count")
            else obj.user.bookings.count()
        )

        if total > 1:
            return format_html(
                '<span class="vivero-badge vivero-badge-repeat">'
                "Recurrente · {} reservas"
                "</span>",
                total,
            )

        return format_html(
            '<span class="vivero-badge vivero-badge-new">{}</span>',
            "Nuevo",
        )

    @admin.display(
        description="Reservas anteriores",
    )
    def previous_bookings(self, obj):
        if not obj.pk:
            return "El historial aparecerá después de guardar la reserva."

        previous = (
            obj.user.bookings
            .exclude(pk=obj.pk)
            .order_by(
                "-check_in",
                "-created_at",
            )[:10]
        )

        if not previous:
            return format_html(
                '<span class="vivero-history-empty">{}</span>',
                "Este huésped no tiene reservas anteriores.",
            )

        booking_items = format_html_join(
            "",
            (
                "<li>"
                "<strong>{} → {}</strong>"
                "<span>{}</span>"
                "<span>{} huésped(es)</span>"
                "</li>"
            ),
            (
                (
                    booking.check_in.strftime("%d/%m/%Y"),
                    booking.check_out.strftime("%d/%m/%Y"),
                    booking.get_status_display(),
                    booking.guests,
                )
                for booking in previous
            ),
        )

        return format_html(
            '<div class="vivero-history">'
            "<ul>{}</ul>"
            "</div>",
            booking_items,
        )

    # =====================================================
    # ACCIONES MASIVAS
    # =====================================================

    def update_booking_status(
        self,
        request,
        queryset,
        status,
        message,
    ):
        updated = queryset.update(
            status=status
        )

        self.message_user(
            request,
            message.format(
                total=updated
            ),
            level=messages.SUCCESS,
        )

    @admin.action(
        description="Marcar como pendientes"
    )
    def mark_as_pending(self, request, queryset):
        self.update_booking_status(
            request=request,
            queryset=queryset,
            status="pending",
            message=(
                "{total} reserva(s) marcada(s) "
                "como pendiente(s)."
            ),
        )

    @admin.action(
        description="Marcar como confirmadas"
    )
    def mark_as_confirmed(self, request, queryset):
        self.update_booking_status(
            request=request,
            queryset=queryset,
            status="confirmed",
            message=(
                "{total} reserva(s) confirmada(s)."
            ),
        )

    @admin.action(
        description="Marcar como canceladas"
    )
    def mark_as_cancelled(self, request, queryset):
        self.update_booking_status(
            request=request,
            queryset=queryset,
            status="cancelled",
            message=(
                "{total} reserva(s) cancelada(s)."
            ),
        )

    @admin.action(
        description="Marcar como finalizadas"
    )
    def mark_as_completed(self, request, queryset):
        self.update_booking_status(
            request=request,
            queryset=queryset,
            status="completed",
            message=(
                "{total} reserva(s) finalizada(s)."
            ),
        )

    class Media:
        css = {
            "all": (
                "core/css/el_vivero_admin.css",
            )
        }
