import os
import logging

import dash
from dash import Dash, dcc, html
from flask import Flask

from _authz import AuthMiddleware

flask_app = Flask(__name__)

DEPLOYENV = os.getenv("DEPLOYENV")
if DEPLOYENV in ("Production", "Dev"):
    from _celery import celery_app
    from dash import CeleryManager

    background_manager = CeleryManager(celery_app, cache_by=lambda: 100, expire=1200)
    flask_app.wsgi_app = AuthMiddleware(flask_app.wsgi_app)
else:
    import diskcache
    from dash import DiskcacheManager

    cache = diskcache.Cache("./cache")
    background_manager = DiskcacheManager(cache)

dash_app = Dash(
    __name__,
    server=flask_app,
    pages_folder="projects",
    serve_locally=False,
    background_callback_manager=background_manager
)

dash_app.layout = dcc.Loading(
    children=html.Div(
        [
            "header",
            html.Div([
                html.Div(
                    dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                ) for page in dash.page_registry.values()
            ]),
            dash.page_container,
            "footer",
        ]
    ),
    fullscreen=True,
)


# health check for k8s
@flask_app.get("/health")
def health():
    return "OK"


class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return '/health' not in record.getMessage() and '/favicon.ico' not in record.getMessage()


# Create a handler for Gunicorn's access logs
gunicorn_access_handler = logging.getLogger('gunicorn.access')

# Add the custom filter to this handler
health_filter = HealthCheckFilter()
gunicorn_access_handler.addFilter(health_filter)

if __name__ == '__main__':
    flask_app.run()
