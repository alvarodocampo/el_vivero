(function () {
    "use strict";

    const rootElement = document.getElementById("my-bookings-app");
    if (!rootElement || !window.React || !window.ReactDOM) return;
    const e = window.React.createElement;

    function formatDate(value) {
        return new Intl.DateTimeFormat("es-ES", {
            day: "2-digit", month: "long", year: "numeric", timeZone: "UTC"
        }).format(new Date(value + "T00:00:00Z"));
    }

    function BookingCard({ booking }) {
        return e("article", { className: "booking-card" },
            e("div", { className: "booking-card-top" },
                e("strong", null, booking.reference),
                e("span", { className: "booking-status booking-status-" + booking.status }, booking.status_label)
            ),
            e("div", { className: "booking-dates" },
                e("div", null, e("span", null, "Entrada"), e("strong", null, formatDate(booking.check_in))),
                e("div", null, e("span", null, "Salida"), e("strong", null, formatDate(booking.check_out)))
            ),
            e("div", { className: "booking-summary" },
                e("span", null, booking.nights + (booking.nights === 1 ? " noche" : " noches")),
                e("span", null, booking.guests + (booking.guests === 1 ? " huésped" : " huéspedes")),
                e("strong", null, booking.total_price + " €")
            )
        );
    }

    function App() {
        const [state, setState] = React.useState({ loading: true, bookings: [], error: "", login: false });

        React.useEffect(function () {
            fetch(rootElement.dataset.apiUrl, { headers: { Accept: "application/json" } })
                .then(function (response) {
                    if (response.status === 401) {
                        setState({ loading: false, bookings: [], error: "", login: true });
                        return null;
                    }
                    if (!response.ok) throw new Error("No se pudieron cargar las reservas.");
                    return response.json();
                })
                .then(function (data) {
                    if (data) setState({ loading: false, bookings: data.bookings, error: "", login: false });
                })
                .catch(function (error) {
                    setState({ loading: false, bookings: [], error: error.message, login: false });
                });
        }, []);

        if (state.loading) return e("p", { className: "bookings-loading" }, "Cargando reservas…");
        if (state.login) return e("div", { className: "bookings-empty" },
            e("p", null, "Inicia sesión para consultar tus reservas."),
            e("a", { href: rootElement.dataset.loginUrl }, "Iniciar sesión")
        );
        if (state.error) return e("p", { className: "bookings-error" }, state.error);
        if (!state.bookings.length) return e("div", { className: "bookings-empty" },
            e("p", null, "Todavía no tienes ninguna reserva."),
            e("a", { href: "/disponibilidad/" }, "Consultar disponibilidad")
        );
        return e("div", { className: "bookings-grid" }, state.bookings.map(function (booking) {
            return e(BookingCard, { key: booking.id, booking: booking });
        }));
    }

    window.ReactDOM.createRoot(rootElement).render(e(App));
}());
