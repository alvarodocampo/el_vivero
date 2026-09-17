# El Vivero

Aplicación web para gestionar las reservas de un alojamiento rural situado en Chiclana de la Frontera. El backend y la administración están desarrollados con Django. La pantalla **Mis reservas** utiliza React y consume datos reales de la API de Django.

## Funciones principales

- Información, fotografías, normas, preguntas frecuentes y contacto.
- Registro e inicio de sesión por correo electrónico.
- Calendario de disponibilidad.
- Reservas asociadas a cada huésped.
- Estancia mínima de dos noches y máximo de cuatro huéspedes.
- Prevención de reservas solapadas.
- Precio por noche y cálculo automático del total.
- Vista React de las reservas del usuario.
- Administración de huéspedes, estados, historial y observaciones internas.

## Tecnologías

- Python 3.13 y Django 6.
- Django Allauth.
- SQLite en desarrollo y PostgreSQL en producción.
- HTML, CSS y JavaScript.
- React 18 para la vista Mis reservas.
- WhiteNoise y Gunicorn para el despliegue.

## Instalación local

```bash
python -m venv venv
```

En Windows:

```bash
venv\Scripts\activate
```

En Linux o macOS:

```bash
source venv/bin/activate
```

Después:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La aplicación estará disponible en `http://127.0.0.1:8000/` y el panel administrativo en `http://127.0.0.1:8000/admin/`.

## Variables de entorno

Consulta `.env.example`. En producción son especialmente importantes:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL`
- `DEFAULT_PRICE_PER_NIGHT`

Nunca publiques el archivo `.env`, credenciales o claves privadas en GitHub.

## Pruebas

```bash
python manage.py test
python manage.py check
python manage.py check --deploy
```

## API utilizada por React

- `GET /api/mis-reservas/`: devuelve las reservas del usuario autenticado.
- `GET /api/fechas-ocupadas/`: devuelve las fechas que no se pueden reservar.
- `POST /api/reservar/`: valida y crea una reserva.

## Despliegue

El archivo `render.yaml` contiene una configuración inicial para Render con PostgreSQL. Antes de desplegar, ajusta `DJANGO_ALLOWED_HOSTS` al dominio definitivo y comprueba que todas las variables de entorno estén configuradas.
