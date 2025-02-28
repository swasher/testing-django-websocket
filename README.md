Demo how websocket works with Django.

Based on `Django Channels` and `daphne`.

Run server with:

    daphne log_app.asgi:application --bind 0.0.0.0 --port 8000

In one window you can post messages, and other window will receive them via web-socket.
